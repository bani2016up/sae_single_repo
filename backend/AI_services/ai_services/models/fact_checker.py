import re

from typing import List, Literal
from tqdm.auto import tqdm
from transformers import RobertaForSequenceClassification, RobertaTokenizer

from ..interfaces import FactCheckerInterface
from ..response import SuggestionResponse
from ..processing import Pipeline


class FactChecker(FactCheckerInterface):
    def __init__(
        self,
        model_name: str = "Dzeniks/roberta-fact-check",
        sentence_processing_pipeline: Pipeline = None,
        paragraph_processing_pipeline: Pipeline = None,
        *,
        device: Literal["cuda", "cpu"] = "cuda",
        tokenizer_kwargs: dict = None,
        model_kwargs: dict = None,
        use_tqdm: bool = False,
    ):
        super().__init__(device=device)

        self.model_name = model_name
        self.tokenizer = RobertaTokenizer.from_pretrained(
            'Dzeniks/roberta-fact-check',
            **(tokenizer_kwargs or {})
        )
        self.model = RobertaForSequenceClassification.from_pretrained(
            'Dzeniks/roberta-fact-check',
            **(model_kwargs or {})
        )

        if paragraph_processing_pipeline is None:
            self.paragraph_processing_pipeline = Pipeline(
                [
                    ("sentence_reg", re.compile(r"(?<!\w\.\w.)(?<![A-Z][a-z]\.)(?<=[.?])\s").split)
                ]
            )
        else:
            self.paragraph_processing_pipeline = paragraph_processing_pipeline

        self.sentence_processing_pipeline = sentence_processing_pipeline or Pipeline()
        self.use_tqdm = use_tqdm

    def to(self, device: Literal["cpu", "cuda"]) -> None:
        self.device = device
        self.model.to(device)
        self.tokenizer.to(device)

    def evaluate_sentence(self, sentence: str, context: str = "") -> List[SuggestionResponse]:
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
