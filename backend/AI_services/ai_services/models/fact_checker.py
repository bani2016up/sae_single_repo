import torch

from tqdm.auto import tqdm
from typing import Any, List, Iterable, Union
from transformers import RobertaForSequenceClassification, RobertaTokenizer

from .explanation import ExplanationLLM
from ..interfaces import (
    FactCheckerInterface,
    DeviceAwareModel,
    VectorStorageInterface,
    LLMInterface
)
from ..response import SuggestionResponse, SuggestionPosition
from ..processing import Pipeline, get_default_paragraph_processing_pipeline
from ..typing import DeviceType

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
        claim: Union[str, Iterable[str]],
        evidence: Union[str, Iterable[str]]
    ) -> torch.Tensor:
        """
        Processes the claim and evidence using the tokenizer and model.
        Args:
            claim (str or Iterable[str]): The claim or claims to evaluate.
            evidence (str or Iterable[str]): The evidence or evidences to evaluate against the claim.
        Returns:
            torch.Tensor: The model outputs.
        Raises:
            ValueError: If claim and evidence have different lengths.
        """
        if isinstance(claim, str):
            claim = [claim]
        if isinstance(evidence, str):
            evidence = [evidence]
        if len(claim) != len(evidence):
            raise ValueError("Claim and evidence must have the same length.")

        inputs = self.tokenizer(
            claim,
            evidence,
            return_tensors="pt"
        ).to(self.device)

        with torch.no_grad():
            outputs = self.model(**inputs)
        return outputs

    forward = __call__  # just in case


class FactCheckerPipeline(FactCheckerInterface, FactCheckingModel):
    def __init__(
        self,
        vector_storage: VectorStorageInterface,
        model_name: str = "Dzeniks/roberta-fact-check",
        sentence_processing_pipeline: Pipeline = None,
        paragraph_processing_pipeline: Pipeline = None,
        llm: LLMInterface = None,
        *,
        storage_search_threshold: float = 1.0,
        storage_search_k: int = 5,
        max_new_tokens: int = 256,
        do_sample: bool = False,
        temperature: float = 0.1,
        device: DeviceType = "cuda",
        tokenizer_kwargs: dict = None,
        model_kwargs: dict = None,
        use_tqdm: bool = False,
        paragraph_processing_device: DeviceType = "cuda",
        sentence_processing_device: DeviceType = "cpu",
        llm_device: DeviceType = "cuda"
    ):
        """
        Initializes the FactCheckerPipeline with a pre-trained model and tokenizer.

        Args:
            vector_storage (VectorStorageInterface): The vector storage for storing and retrieving evidence.
            model_name (str): The name of the pre-trained model.
            sentence_processing_pipeline (Pipeline): The pipeline for processing sentences.
            paragraph_processing_pipeline (Pipeline): The pipeline for processing paragraphs.
            device (str): The device to use for computation ("cuda" or "cpu").
            paragraph_processing_device (str): Device for paragraph processing ("cuda" or "cpu").
            sentence_processing_device (str): Device for sentence processing ("cuda" or "cpu").
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
        """
        super().__init__(
            model_name=model_name,
            device=device,
            tokenizer_kwargs=tokenizer_kwargs,
            model_kwargs=model_kwargs,
            use_tqdm=use_tqdm
        )

        self.llm = (llm or ExplanationLLM()).to(llm_device)
        self.paragraph_processing_pipeline = (
                paragraph_processing_pipeline or get_default_paragraph_processing_pipeline()
        ).to(paragraph_processing_device)
        self.sentence_processing_pipeline = (
                sentence_processing_pipeline or Pipeline()
        ).to(sentence_processing_device)

        self.vector_storage = vector_storage
        self.storage_search_k = storage_search_k
        self.storage_search_threshold = storage_search_threshold
        self.max_new_tokens = max_new_tokens
        self.do_sample = do_sample
        self.temperature = temperature

    def evaluate_sentence(self, sentence: str, context: str = "") -> List[SuggestionResponse]:
        """
        Evaluate a single sentence.

        Args:
            sentence (str): The sentence to evaluate.
            context (str): Additional context for the evaluation.
        Returns:
            List[SuggestionResponse]: A list of SuggestionResponse instances for the evaluated sentence.
        """
        # HACK
        # FIXME: context? for what?
        # TODO: fact checking with NER
        # TODO: in_original=True
        metadata = self.vector_storage.search(
            sentence,
            k=self.storage_search_k,
            threshold=self.storage_search_threshold
        )

        if len(metadata) == 0:
            return []

        historical_data = self._metadata2text(metadata)
        result = self.forward(sentence, historical_data)

        if result[0].item() == 0:
            return []

        return [
            SuggestionResponse(
                fact=sentence,
                is_correct=result[0].item(),
                position=SuggestionPosition(
                    start_char_index=0,
                    end_char_index=len(sentence),
                    in_original=False
                ),
                explanation=self.llm(
                    claim=sentence,
                    evidence=historical_data,
                    max_new_tokens=self.max_new_tokens,
                    do_sample=self.do_sample,
                    temperature=self.temperature
                )
            )
        ]

    def evaluate_text(self, text: str, *, context: str = "") -> List[SuggestionResponse]:
        """
        Evaluate a given text and return a list of suggestion responses.

        Args:
            text (str): The text to evaluate.
            context (str): Additional context for the evaluation.
        Returns:
            List[SuggestionResponse]: A list of SuggestionResponse instances for the evaluated text.
        """
        sentences = self.paragraph_processing_pipeline(text)
        if self.use_tqdm:
            sentences = tqdm(
                sentences,
                desc="Processing sentences",
                total=len(sentences),
                unit="sentence"
            )
        result = []
        for sentence in sentences:
            sentence = self.sentence_processing_pipeline(sentence)
            if len(sentence) > 0:
                result.extend(self.evaluate_sentence(sentence, context=context))
        return result

    @staticmethod
    def _metadata2text(metadata: list[dict[str, Any]]) -> str:
        return ".".join([text['metadata']['text'] for text in metadata])
