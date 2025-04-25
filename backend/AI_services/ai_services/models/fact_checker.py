import torch

from tqdm.auto import tqdm
from typing import Any, List, Literal, Iterable, Union
from transformers import RobertaForSequenceClassification, RobertaTokenizer

from ..interfaces import (
    FactCheckerInterface,
    DeviceAwareModel,
    VectorStorageInterface
)
from ..response import SuggestionResponse
from ..processing import Pipeline, get_default_paragraph_processing_pipeline

__all__ = (
    "FactCheckingModel",
    "FactCheckerPipeline"
)


class FactCheckingModel(DeviceAwareModel):
    def __init__(
        self,
        model_name: str = "Dzeniks/roberta-fact-check",
        *,
        device: Literal["cuda", "cpu"] = "cuda",
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
        self.tokenizer.to(device)

    def to(self, device: Literal["cpu", "cuda"]) -> "FactCheckingModel":
        """
        Moves the model and tokenizer to the specified device.
        Args:
            device (str): The device to move the model and tokenizer to ("cuda" or "cpu").
        Returns:
            FactCheckingModel: The updated model instance.
        """
        self._device = device
        self.model.to(device)
        self.tokenizer.to(device)
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
        # TODO: Handle with custom classes
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
        *,
        device: Literal["cuda", "cpu"] = "cuda",
        tokenizer_kwargs: dict = None,
        model_kwargs: dict = None,
        use_tqdm: bool = False,
        paragraph_processing_device: Literal["cuda", "cpu"] = "cuda",
        sentence_processing_device: Literal["cuda", "cpu"] = "cpu"
    ):
        """
        Initializes the FactCheckerPipeline with a pre-trained model and tokenizer.

        Args:
            vector_storage (VectorStorageInterface): The vector storage for storing and retrieving evidence.
            model_name (str): The name of the pre-trained model.
            sentence_processing_pipeline (Pipeline): The pipeline for processing sentences.
            paragraph_processing_pipeline (Pipeline): The pipeline for processing paragraphs.
            device (str): The device to use for computation ("cuda" or "cpu").
            tokenizer_kwargs (dict): Additional arguments for the tokenizer.
            model_kwargs (dict): Additional arguments for the model.
            use_tqdm (bool): Whether to use tqdm for progress bars.
            paragraph_processing_device (str): Device for paragraph processing ("cuda" or "cpu").
            sentence_processing_device (str): Device for sentence processing ("cuda" or "cpu").
        """
        super().__init__(
            model_name=model_name,
            device=device,
            tokenizer_kwargs=tokenizer_kwargs,
            model_kwargs=model_kwargs,
            use_tqdm=use_tqdm
        )

        self._paragraph_processing_device = paragraph_processing_device
        self._sentence_processing_device = sentence_processing_device

        self.paragraph_processing_pipeline = (
                paragraph_processing_pipeline or get_default_paragraph_processing_pipeline()
        )
        self.sentence_processing_pipeline = (
                sentence_processing_pipeline or Pipeline()
        )
        self.vector_storage = vector_storage

        self.paragraph_processing_pipeline.to(paragraph_processing_device)
        self.sentence_processing_pipeline.to(sentence_processing_device)

    def evaluate_sentence(self, sentence: str, context: str = "") -> List[SuggestionResponse]:
        # HACK
        # FIXME: context? for what?
        # TODO: add k to the constructor
        # TODO: result -> SuggestionResponse
        raise NotImplementedError("evaluate_sentence is not implemented.")
        metadata = self.vector_storage.search(sentence, k=5)
        if len(metadata) == 0:
            return []
        historical_data = self._metadata2text(metadata)
        result = self.forward(sentence, historical_data)

    def evaluate_text(self, text: str, *, context: str = "") -> List[SuggestionResponse]:
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

    # XXX: property -> self.something_to(...)
    @property
    def paragraph_processing_device(self) -> Literal["cuda", "cpu"]:
        return self._paragraph_processing_device

    @paragraph_processing_device.setter
    def paragraph_processing_device(self, device: Literal["cuda", "cpu"]):
        self._paragraph_processing_device = device
        self.paragraph_processing_pipeline.to(device)

    @property
    def sentence_processing_device(self) -> Literal["cuda", "cpu"]:
        return self._sentence_processing_device

    @sentence_processing_device.setter
    def sentence_processing_device(self, device: Literal["cuda", "cpu"]):
        self._sentence_processing_device = device
        self.sentence_processing_pipeline.to(device)

    @staticmethod
    def _metadata2text(metadata: list[dict[str, Any]]) -> str:
        return ".".join([text['metadata']['text'] for text in metadata])
