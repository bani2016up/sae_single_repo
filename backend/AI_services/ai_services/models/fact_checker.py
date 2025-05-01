import torch

from tqdm.auto import tqdm
from typing import List, Callable, Union
from transformers import RobertaForSequenceClassification, RobertaTokenizer

from .explanation import ExplanationLLM
from ..interfaces import (
    FactCheckerInterface,
    DeviceAwareModel,
    VectorStorageInterface,
    LLMInterface
)
from ..response import SuggestionResponse, SuggestionPosition
from ..preprocessing import Pipeline, get_default_paragraph_processing_pipeline
from ..typing import DeviceType, DocumentMetadataType
from ..sentence import SentenceProposal

__all__ = (
    "FactCheckingModel",
    "FactCheckerPipeline"
)


class FactCheckingModel(DeviceAwareModel):
    def __init__(
        self,
        model_name: str = "Dzeniks/roberta-fact-check",
        *,
        device: DeviceType = "cuda",
        tokenizer_kwargs: dict = None,
        model_kwargs: dict = None,
        use_tqdm: bool = False
    ):
        """
        Initializes the FactCheckingModel with a pre-trained model and tokenizer.
        Args:
            model_name (str): The name of the pre-trained model.
            device (str): The device to use for computation ("cuda" or "cpu").
            tokenizer_kwargs (dict): Additional arguments for the tokenizer.
            model_kwargs (dict): Additional arguments for the model.
            use_tqdm (bool): Whether to use tqdm for progress bars.
        """
        super().__init__(device=device)
        self.use_tqdm = use_tqdm
        self.tokenizer = RobertaTokenizer.from_pretrained(
            model_name, **(tokenizer_kwargs or {})
        )
        self.model = RobertaForSequenceClassification.from_pretrained(
            model_name, **(model_kwargs or {})
        )
        self.model.eval()
        self.model.to(device)

    def to(self, device: DeviceType) -> "FactCheckingModel":
        """
        Moves the model and tokenizer to the specified device.
        Args:
            device (str): The device to move the model and tokenizer to ("cuda" or "cpu").
        Returns:
            FactCheckingModel: The updated model instance.
        """
        self._device = device
        self.model.to(device)
        return self

    def __call__(
        self,
        claim: str,
        evidence: str
    ) -> torch.Tensor:
        """
        Evaluates a claim against evidence using the pre-trained model.

        Args:
            claim (str): The claim to be evaluated.
            evidence (str): The evidence to support or refute the claim.
        Returns:
            torch.Tensor: The model's output logits.
        """
        inputs = self.tokenizer.encode_plus(
            claim,
            evidence,
            return_tensors="pt",
            truncation=True,
            padding=True,
            max_length=512 # TODO: use config from __init__
        ).to(self.device)

        with torch.no_grad():
            outputs = self.model(**inputs)

        return outputs


class FactCheckerPipeline(FactCheckerInterface, FactCheckingModel):
    """
    A flexible, modular pipeline for evaluating claims using a pre-trained fact-checking model.
    It integrates evidence retrieval via vector storage, generates explanations with
    a language model, and supports scalable, customizable processing for
    diverse fact-checking and NLP tasks.
    """

    def __init__(
        self,
        vector_storage: VectorStorageInterface,
        model_name: str = "Dzeniks/roberta-fact-check",
        processing_pipeline: Pipeline = None,
        llm: LLMInterface = None,
        *,
        storage_search_threshold: float = 1.0,
        storage_search_k: int = 5,
        max_new_tokens: int = 256,
        do_sample: bool = False,
        temperature: float = 0.1,
        device: DeviceType = "cpu",
        tokenizer_kwargs: dict = None,
        model_kwargs: dict = None,
        use_tqdm: bool = False,
        processing_device: DeviceType = None,
        llm_device: DeviceType = None,
        context_token: str = "</CONTEXT>",
        get_explanation: bool = True,
        automatic_contextualisation: bool = False
    ):
        """
        Initializes the FactCheckerPipeline with a pre-trained model and tokenizer.

        Args:
            vector_storage (VectorStorageInterface): The vector storage for storing and retrieving evidence.
            model_name (str): The name of the pre-trained model.
            processing_pipeline (Pipeline): The pipeline for processing paragraphs.
            device (str): The device to use for computation ("cuda" or "cpu").
            processing_device (str): Device for paragraph processing ("cuda" or "cpu").
            llm_device (str): Device for the language model ("cuda" or "cpu").
            tokenizer_kwargs (dict): Additional arguments for the tokenizer.
            model_kwargs (dict): Additional arguments for the model.
            use_tqdm (bool): Whether to use tqdm for progress bars.
            llm (LLMInterface): The language model for generating explanations.
            storage_search_threshold (float): The threshold for searching in the vector storage.
            storage_search_k (int): The number of nearest neighbors to search for in the vector storage.
            max_new_tokens (int): Maximum number of tokens to generate for the explanation.
            do_sample (bool): Whether to sample from the distribution.
            temperature (float): Sampling temperature for the explanation generation.
            context_token (str): Token to separate context from the sentence.
            get_explanation (bool): Whether to generate an explanation.
            automatic_contextualisation (bool): Whether to automatically contextualize the claim.
        """
        super().__init__(
            model_name=model_name,
            device=device,
            tokenizer_kwargs=tokenizer_kwargs,
            model_kwargs=model_kwargs,
            use_tqdm=use_tqdm
        )
        self.context_setter: Union[Callable[..., None], None] = None

        if automatic_contextualisation:
            pipeline_coref_system_tokens = getattr(
                processing_pipeline, "system_tokens", None
            )  # type: Union[list[str], None]

            if pipeline_coref_system_tokens is not None:
                if context_token not in pipeline_coref_system_tokens:
                    pipeline_coref_system_tokens.append(context_token)

            self.context_setter = getattr(processing_pipeline, "set_context", None)

            if hasattr(processing_pipeline, "set_context_token"):
                getattr(processing_pipeline, "set_context_token")(context_token)

        if processing_device is None:
            processing_device = device

        if llm_device is None:
            llm_device = device

        if get_explanation:
            self.llm = (llm or ExplanationLLM()).to(llm_device)
        else:
            def dummy_llm(*_, **_kwargs) -> str:
                # PEP 8 — Naming Styles:
                # _single_leading_underscore: weak “internal use” indicator.
                # E.g. from M import * does not import objects whose names start with an underscore.
                # See https://peps.python.org/pep-0008/#descriptive-naming-styles
                return ""

            self.llm = dummy_llm

        self.processing_pipeline = (
                processing_pipeline or get_default_paragraph_processing_pipeline()
        ).to(processing_device)

        self.vector_storage = vector_storage
        self.storage_search_k = storage_search_k
        self.storage_search_threshold = storage_search_threshold
        self.max_new_tokens = max_new_tokens
        self.do_sample = do_sample
        self.temperature = temperature
        self.context_token = context_token

    def _predict(self, claim: str, *, is_original: bool = False) -> List[SuggestionResponse]:
        # TODO: fact checking with NER
        metadata = self.vector_storage.search(
            str(claim),
            k=self.storage_search_k,
            threshold=self.storage_search_threshold
        )
        historical_data = self._metadata2text(metadata)

        if len(historical_data) < 10:
            return []

        result = super().__call__(str(claim), historical_data)

        if torch.argmax(result[0], dim=1).item() == 0:
            return []

        explanation = self.llm(
            claim=str(claim),
            evidence=historical_data,
            max_new_tokens=self.max_new_tokens,
            do_sample=self.do_sample,
            temperature=self.temperature
        )

        return [
            self._sentence2response(
                claim=claim,
                is_correct=False,
                explanation=explanation,
                is_original=is_original
            )
        ]

    def evaluate_sentence(self, sentence: str, context: str = "") -> List[SuggestionResponse]:
        """
        Evaluate a single sentence.

        Args:
            sentence (str): The sentence to evaluate.
            context (str): Additional context for the evaluation.
        Returns:
            List[SuggestionResponse]: A list of SuggestionResponse instances for the evaluated sentence.
        """
        if self.context_setter is not None:
            self.context_setter(context)

        sentence_with_context = self.processing_pipeline(sentence)[0]

        if len(sentence_with_context) == 0:
            return []

        result = self._predict(sentence, is_original=False)

        if result is None:
            return []

        return result

    def evaluate_text(self, text: str, *, context: str = "") -> List[SuggestionResponse]:
        """
        Evaluate a given text and return a list of suggestion responses.

        Args:
            text (str): The text to evaluate.
            context (str): Additional context for the evaluation.
        Returns:
            List[SuggestionResponse]: A list of SuggestionResponse instances for the evaluated text.
        """
        if self.context_setter is not None:
            self.context_setter(context)

        sentences = self.processing_pipeline(text)  # type: list[str]

        if len(sentences) == 0:
            return []

        results = []
        for sentence in tqdm(sentences, desc="Evaluating sentences", disable=not self.use_tqdm):
            if len(sentence) == 0:
                continue
            result = self._predict(sentence, is_original=True)
            if result is not None:
                results.extend(result)
        return results

    @staticmethod
    def _metadata2text(metadata: List[DocumentMetadataType]) -> str:
        return ".".join([text['metadata']['text'] for text in metadata])

    @staticmethod
    def _sentence2response(
        claim: Union[SentenceProposal, str],
        is_correct: Union[int, bool],
        explanation: str,
        is_original: bool = False
    ) -> SuggestionResponse:
        if isinstance(claim, SentenceProposal):
            return SuggestionResponse(
                fact=str(claim),
                is_correct=is_correct,
                position=SuggestionPosition(
                    start_char_index=claim.tokens[0].start,
                    end_char_index=claim.tokens[-1].end,
                    in_original=is_original
                ),
                explanation=explanation
            )
        return SuggestionResponse(
            fact=claim,
            is_correct=is_correct,
            position=SuggestionPosition(
                start_char_index=0,
                end_char_index=len(claim),
                in_original=False
            ),
            explanation=explanation
        )

    __call__ = evaluate_text
