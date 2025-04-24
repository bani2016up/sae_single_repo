import torch

from tqdm.auto import tqdm
from typing import List, Literal, Iterable, Union
from transformers import RobertaForSequenceClassification, RobertaTokenizer

from ..interfaces import FactCheckerInterface, DeviceAwareModel, VectorStorageInterface
from ..response import SuggestionResponse
from ..processing import Pipeline, get_default_paragraph_processing_pipeline


class FactCheckingModelBase(DeviceAwareModel):
    def __init__(
        self,
        model_name: str = "Dzeniks/roberta-fact-check",
        *,
        device: Literal["cuda", "cpu"] = "cuda",
        tokenizer_kwargs: dict = None,
        model_kwargs: dict = None,
        use_tqdm: bool = False
    ):
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

    def to(self, device: Literal["cpu", "cuda"]) -> "FactCheckingModelBase":
        self.device = device
        self.model.to(device)
        self.tokenizer.to(device)
        return self

    def __call__(
        self,
        claim: Union[str, Iterable[str]],
        evidence: Union[str, Iterable[str]]
    ) -> torch.Tensor:
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


class FactChecker(FactCheckerInterface, FactCheckingModelBase):
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
        # TODO: Implement the logic to evaluate a single sentence
        pass

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
