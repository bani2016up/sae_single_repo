"""
Coreference resolution using LingMessCoref.

This module provides a class for coreference resolution that inherits from DeviceAwareModel.
The main interface is the __call__ method, which replaces all mentions in each coreference
cluster with the first mention (antecedent).
"""

from fastcoref import LingMessCoref
from ai_services.interfaces import DeviceAwareModel

class LingMessCorefResolver(DeviceAwareModel):
    """
    Coreference resolver using the LingMessCoref model.
    Inherits from DeviceAwareModel.
    """

    def __init__(self, model_name: str = "biu-nlp/lingmess-coref", enable_progress_bar: bool = False, device: str = "cpu"):
        """
        Initialize the LingMessCoref model.

        Args:
            model_name (str): The name or path of the LingMessCoref model.
            enable_progress_bar (bool): Whether to show the progress bar during inference.
            device (str): Device to load the model on ("cpu" or "cuda").
        """
        super().__init__(device=device)
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

        replacements.sort(key=lambda x: x[0], reverse=True)

        new_text = text
        for start, end, rep in replacements:
            new_text = new_text[:start] + rep + new_text[end:]

        return new_text

if __name__ == '__main__':
    sample = "Angela went to the park. She saw her friend there. Angela and her friend talked for hours."
    print("Before:\n", sample)
    resolver = LingMessCorefResolver()
    print("\nAfter:\n", resolver(sample))
