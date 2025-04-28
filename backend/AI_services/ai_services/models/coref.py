"""
Coreference resolution using LingMessCoref(by default).

This module provides a class for coreference resolution that inherits from DeviceAwareModel.
The main interface is the __call__ method, which replaces all mentions in each coreference
cluster with the first mention (antecedent).
"""

import logging

from dataclasses import dataclass
from fastcoref import LingMessCoref

from ..interfaces import DeviceAwareModel
from ..typing import DeviceType

__all__ = ("CorefResolver",)


@dataclass(frozen=True, repr=True, kw_only=True)
class CorefResponse(object):
    text: str
    antecedents: list[str]


class CorefResolver(DeviceAwareModel):
    """
    Coreference resolver using the LingMessCoref(by default) model.
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
        use_logger: bool = False
    ):
        """
        Initialize the coreference model.

        Args:
            model_name (Optional[str]): The name or path of the Coref model. Defaults to "biu-nlp/lingmess-coref".
            enable_progress_bar (bool): Whether to show the progress bar during inference.
            device (DeviceType): Device to load the model on ("cpu" or "cuda").
        """
        self._set_fastcoref_logger(use_logger)
        super().__init__(device=device)
        self.model_name = model_name
        self.enable_progress_bar = enable_progress_bar
        self.model = LingMessCoref(model_name, enable_progress_bar=enable_progress_bar, device=device)

    def __call__(self, text: str) -> CorefResponse:
        """
        Replace all mentions in each coreference cluster with the first mention (antecedent).

        Args:
            text (str): The input text to process.

        Returns:
            CorefResponse: A dataclass containing the modified text and a list of antecedents.
        """
        result = self.model.predict(text)
        clusters = result.get_clusters(as_strings=False)

        replacements = []
        antecedents = []
        for cluster in clusters:
            start0, end0 = cluster[0]
            antecedent = text[start0:end0]
            for start, end in cluster[1:]:
                replacements.append((start, end, antecedent))
            antecedents.append(antecedent)

        replacements.sort(key=lambda x: x[0], reverse=True)

        new_text = list(text)
        for start, end, rep in replacements:
            new_text[start:end] = rep

        new_text = "".join(new_text)
        return CorefResponse(text=new_text, antecedents=antecedents)

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
