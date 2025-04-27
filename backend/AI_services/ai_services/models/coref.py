"""
Coreference resolution using LingMessCoref.

This module provides a class for coreference resolution that inherits from DeviceAwareModel.
The main interface is the __call__ method, which replaces all mentions in each coreference
cluster with the first mention (antecedent).
"""

from fastcoref import LingMessCoref
from ..interfaces import DeviceAwareModel
from ..typing import DeviceType

__all__ = ("CorefResolver",)

class CorefResolver(DeviceAwareModel):
    """
    Coreference resolver using the LingMessCoref(dy default) model.
    Inherits from DeviceAwareModel.
    """

    def __init__(
        self,
        model_name: str = "biu-nlp/lingmess-coref",
        *,
        enable_progress_bar: bool = False,
        device: DeviceType = "cpu"
    ):
        """
        Initialize the coreference model.

        Args:
            model_name (Optional[str]): The name or path of the Coref model. Defaults to "biu-nlp/lingmess-coref".
            enable_progress_bar (bool): Whether to show the progress bar during inference.
            device (DeviceType): Device to load the model on ("cpu" or "cuda").
        """
        super().__init__(device=device)
        self.model_name = model_name
        self.enable_progress_bar = enable_progress_bar
        self.model = LingMessCoref(model_name, enable_progress_bar=enable_progress_bar)

    def __call__(self, text: str) -> str:
        """
        Replace all mentions in each coreference cluster with the first mention (antecedent).

        Args:
            text (str): The input text to process.

        Returns:
            str: The text with all coreference clusters replaced by their antecedents.
        """
        result = self.model.predict(text)
        clusters = result.get_clusters(as_strings=False)

        replacements = []
        for cluster in clusters:
            start0, end0 = cluster[0]
            antecedent = text[start0:end0]
            for start, end in cluster[1:]:
                replacements.append((start, end, antecedent))

        # Sort replacements by their start index in reverse order to avoid shifting issues
        replacements.sort(key=lambda x: x[0], reverse=True)

        new_text = list(text)
        for start, end, rep in replacements:
            new_text[start:end] = rep

        return "".join(new_text)

    def to(self, device: DeviceType) -> "CorefResolver":
        """
        Move the model to the specified device.

        Args:
            device (DeviceType): The target device ("cpu" or "cuda").

        Returns:
            CorefResolver: self
        """
        self._device = device
        if hasattr(self.model, "to"):
            self.model.to(device)
        return self
