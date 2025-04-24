"""
This module defines a coreference resolution model interface and a concrete implementation
using the biu-nlp/lingmess-coref model from fastcoref.

Classes:
    - CoreferenceResolverInterface: Abstract base class for coreference resolution models.
    - LingMessCoreferenceResolver: Concrete implementation using LingMessCoref.
"""

from abc import ABC, abstractmethod
from typing import Any, List, Tuple

from fastcoref import LingMessCoref

__all__ = (
    "CoreferenceResolverInterface",
    "LingMessCoreferenceResolver",
)


class CoreferenceResolverInterface(ABC):
    """
    Abstract base class for coreference resolution models.

    Defines a common interface for resolving coreference clusters in text.
    """

    def __init__(self, model_name: str):
        """
        Initialize the coreference resolver with the specified model name.

        Args:
            model_name (str): The name or path of the coreference model to use.
        """
        self.model_name = model_name

    @abstractmethod
    def __call__(self, text: str) -> str:
        """
        Process the input text and resolve coreference clusters.

        Args:
            text (str): The input text to process.

        Returns:
            str: The text with coreference clusters replaced.
        """
        ...


class LingMessCoreferenceResolver(CoreferenceResolverInterface):
    """
    Concrete coreference resolver using the biu-nlp/lingmess-coref model from fastcoref.
    """

    def __init__(self, model_name: str = "biu-nlp/lingmess-coref", enable_progress_bar: bool = False):
        """
        Initialize the LingMessCoref model.

        Args:
            model_name (str): The name or path of the LingMessCoref model.
            enable_progress_bar (bool): Whether to show the progress bar during inference.
        """
        super().__init__(model_name)
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
        clusters: List[List[Tuple[int, int]]] = result.get_clusters(as_strings=False)

        # Prepare replacements: (start, end, antecedent)
        replacements = []
        for cluster in clusters:
            start0, end0 = cluster[0]
            antecedent = text[start0:end0]
            for start, end in cluster[1:]:
                replacements.append((start, end, antecedent))

        # Sort replacements in reverse order to avoid messing up indices
        replacements.sort(key=lambda x: x[0], reverse=True)

        new_text = text
        for start, end, rep in replacements:
            new_text = new_text[:start] + rep + new_text[end:]

        return new_text


if __name__ == '__main__':
    # Example usage
    sample = "Angela went to the park. She saw her friend there. Angela and her friend talked for hours."
    print("Before:\n", sample)
    resolver = LingMessCoreferenceResolver()
    print("\nAfter:\n", resolver(sample))
