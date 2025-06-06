from copy import deepcopy
from typing import Callable, List, Dict, TypeAlias, Union
from datasets.utils.logging import disable_progress_bar

from .interfaces import PromptInterface
from .static import FACT_CHECKER_PROMPT
from .typing import PromptType

__all__ = (
    "PromptGeneratorType",
    "FactCheckerPrompt",
    "disable_fastcoref_progress_bar"
)

# can't be placed in typing.py because of circular import (.interfaces -> .typing -> .interfaces)
PromptGeneratorType: TypeAlias = Union[PromptInterface, Callable[[..., str], PromptType]]


class FactCheckerPrompt(PromptInterface):
    """
    A class for generating prompts for fact-checking tasks.
    This class can be used to create prompts for language models
    to evaluate claims and evidence.
    It can be initialized with a base prompt or use a default one.
    The class provides a callable interface to generate the prompt
    by formatting the base prompt with the provided claim and evidence.
    The prompt can be a string or a list of dictionaries,
    where each dictionary represents a message with a role and content.
    The class is designed to be flexible and allows for easy customization
    of the prompt structure.
    """

    def __init__(self, base_prompt: PromptType = None) -> None:
        """
        Initializes the FactCheckerPrompt with a base prompt.
        If no base prompt is provided, a default prompt is used.
        The base prompt can be a string or a list of dictionaries,
        where each dictionary contains a role and content.

        Args:
            base_prompt (Union[str, List[Dict[str, str]]]): The base prompt to use.
                If None, the default FACT_CHECKER_PROMPT is used.
        """
        if base_prompt is None:
            base_prompt = deepcopy(FACT_CHECKER_PROMPT)
        self.base_prompt = base_prompt

    def __call__(self, claim: str, evidence: str) -> PromptType:
        """
        Generates a prompt for the given claim and evidence.
        The prompt is created by formatting the base prompt with the provided claim and evidence.
        The base prompt can be a string or a list of dictionaries.
        If the base prompt is a string, it is formatted directly.
        If the base prompt is a list of dictionaries,
        the last dictionary in the list is updated with the formatted content.

        Args:
            claim (str): The claim to evaluate.
            evidence (str): The evidence to evaluate against the claim.
        """
        prompt = deepcopy(self.base_prompt)
        if isinstance(prompt, str):
            return prompt.format(claim=claim, evidence=evidence)
        item = prompt[-1]
        if isinstance(item, dict):
            item["content"] = item["content"].format(claim=claim, evidence=evidence)
        else:
            raise ValueError("The last item in the prompt list must be a dictionary.")
        return prompt

def disable_fastcoref_progress_bar() -> None:
    disable_progress_bar()