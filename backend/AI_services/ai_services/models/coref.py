"""
    Coreference resolution using the LingMessCoref model.
    This module provides a class `CorefResolver` that uses the LingMessCoref model
"""

import logging
import re

from typing import List
from fastcoref import LingMessCoref

from ..interfaces import DeviceAwareModel
from ..typing import DeviceType
from ..sentence import SentenceProposal, Token

__all__ = ("CorefResolver",)


class CorefResolver(DeviceAwareModel):
    """
    Coreference resolution using the LingMessCoref model.
    This class provides methods to resolve coreferences in a given text.
    It uses the LingMessCoref model for coreference resolution and provides
    methods to tokenize the text, replace coreferences with their canonical mentions,
    and return the resolved sentences as `SentenceProposal` objects.
    """

    @staticmethod
    def _set_fastcoref_logger(enabled: bool) -> None:
        """
        Enable or disable the fastcoref logger.
        """
        level = logging.INFO if enabled else logging.WARNING
        logging.getLogger("fastcoref").setLevel(level)

    def __init__(
        self,
        model_name: str = "biu-nlp/lingmess-coref",
        *,
        enable_progress_bar: bool = False,
        device: DeviceType = "cpu",
        use_logger: bool = False,
        splitter: str = r"(?<!\w\.\w.)(?<![A-Z][a-z]\.)(?<=[.?])\s",
        context_token: str = "</CONTEXT>",
    ):
        """
        Initialize the coreference model.

        Args:
            model_name (Optional[str]): The name or path of the Coref model. Defaults to "biu-nlp/lingmess-coref".
            enable_progress_bar (bool): Whether to show the progress bar during inference.
            device (DeviceType): Device to load the model on ("cpu" or "cuda").
            use_logger (bool): Whether to enable the fastcoref logger.
        """
        super().__init__(device=device)
        self._set_fastcoref_logger(use_logger)
        # tokens are not used in the current implementation
        self.system_tokens = [context_token]  # type: List[str]
        self.model_name = model_name
        self.enable_progress_bar = enable_progress_bar
        self.model = LingMessCoref(model_name, enable_progress_bar=enable_progress_bar, device=device)
        self.splitter = re.compile(splitter)
        self._context_token = context_token
        self._context = ""

    def __call__(self, text: str) -> List[SentenceProposal]:
        """
        Perform coreference resolution on the given text.
        This method takes a text input, processes it using the LingMessCoref model,
        and returns a list of resolved sentences as `SentenceProposal` objects.
        The method first tokenizes the text, then applies coreference resolution,
        and finally replaces coreferences with their canonical mentions.
        
        Args:
            text (str): The input text to resolve coreferences in.
        """
        raw_text = text
        prefix = f"{self._context}\n\n{self._context_token} "
        full_text = prefix + raw_text

        result = self.model.predict(full_text)

        clusters = result.get_clusters()
        clusters_spans = result.get_clusters(as_strings=False)

        adjusted_clusters: List[List[str]] = []
        adjusted_spans: List[List[tuple]] = []
        offset = len(prefix)
        for mentions, spans in zip(clusters, clusters_spans):
            new_spans = [
                (start - offset, end - offset)
                for (start, end) in spans
                if start >= offset
            ]
            if new_spans:
                adjusted_clusters.append(mentions)
                adjusted_spans.append(new_spans)

        antecedents = [
            mention
            for cluster in adjusted_clusters
            for mention in cluster
            if " " in mention
        ]
        antecedents.extend(self.system_tokens)

        tokens_grouped_by_sentences = self._tokenize_text_by_sentences(raw_text, antecedents)

        tokens_with_replacements = self._replace_coreference_by_spans(
            tokens_grouped_by_sentences,
            adjusted_clusters,
            adjusted_spans
        )

        return [
            SentenceProposal(tokens=sent_tokens, index=i)
            for i, sent_tokens in enumerate(tokens_with_replacements)
        ]

    def set_context(self, context: str) -> None:
        """
        Set the context for coreference resolution.
        This context is used to provide additional information
        for resolving coreferences in the input text.

        Args:
            context (str): The context to set.

        """
        self._context = context

    def set_context_token(self, context_token: str) -> None:
        """
        Set the context token for coreference resolution.
        This token is used to indicate the start of the context in the input text.

        Args:
            context_token (str): The context token to set.

        """
        self._context_token = context_token

    def to(self, device: DeviceType) -> "CorefResolver":
        """
        Move the model to the specified device.

        Args:
            device (DeviceType): The target device ("cpu" or "cuda").

        Returns:
            CorefResolver: self
        """
        self._device = device
        if hasattr(self.model.model, "to"):
            self.model.model.to(device)
        return self

    @staticmethod
    def _tokenize_text_with_antecedents(text: str, antecedents: List[str]) -> List[Token]:
        escaped_antecedents = sorted(
            (re.escape(antecedent) for antecedent in antecedents),
            key=len,
            reverse=True
        )
        pattern = (
            rf"({'|'.join(escaped_antecedents)})"
            r"|(\w+[^\w\s]*)"
            r"|([^\w\s])"
        )
        compiled_pattern = re.compile(pattern)

        tokens: List[Token] = []

        for match in compiled_pattern.finditer(text):
            token_text = match.group(0)
            token_start, token_end = match.span(0)
            tokens.append(Token(token_text, token_start, token_end))

        return tokens

    def _tokenize_text_by_sentences(
        self,
        text: str,
        antecedents: List[str]
    ) -> List[List[Token]]:
        tokens_grouped_by_sentences = []  # type: List[List[Token]]
        last_split_position = 0

        for match in self.splitter.finditer(text):
            sentence_end_position = match.start() + 1
            sentence_text = text[last_split_position:sentence_end_position]

            tokens_in_sentence = self._tokenize_text_with_antecedents(sentence_text, antecedents)

            for token in tokens_in_sentence:
                token.start += last_split_position
                token.end += last_split_position

            tokens_grouped_by_sentences.append(tokens_in_sentence)
            last_split_position = match.end()

        if last_split_position < len(text):
            sentence_text = text[last_split_position:]
            tokens_in_last_sentence = self._tokenize_text_with_antecedents(sentence_text, antecedents)

            for token in tokens_in_last_sentence:
                token.start += last_split_position
                token.end += last_split_position

            tokens_grouped_by_sentences.append(tokens_in_last_sentence)

        return tokens_grouped_by_sentences

    @staticmethod
    def _replace_coreference_by_spans(
        tokens_grouped_by_sentence: List[List[Token]],
        coreference_clusters: List[List[str]],
        coreference_clusters_spans: List[List[tuple]]
    ) -> List[List[Token]]:

        start_position_to_canonical_mention = {}
        for cluster_mentions, cluster_spans in zip(coreference_clusters, coreference_clusters_spans):
            canonical_mention = cluster_mentions[0]
            for span in cluster_spans:
                start_position = span[0]
                start_position_to_canonical_mention[start_position] = canonical_mention

        for sentence_tokens in tokens_grouped_by_sentence:
            for token in sentence_tokens:
                if token.start in start_position_to_canonical_mention:
                    canonical_mention = start_position_to_canonical_mention[token.start]

                    matching_span = next(
                        span
                        for spans_list in coreference_clusters_spans
                        for span in spans_list
                        if span[0] == token.start
                    )

                    original_span_length = matching_span[1] - matching_span[0]
                    suffix_text = token.text[original_span_length:]
                    token.text = canonical_mention + suffix_text

        return tokens_grouped_by_sentence
