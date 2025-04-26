from copy import deepcopy
from typing import List, Dict, Union

from .models.fact_checker import FactCheckerPipeline
from .interfaces import PromptInterface
from .static import FACT_CHECKER_PROMPT


class FactCheckerPrompt(PromptInterface):
    def __init__(self, base_prompt: Union[str, List[Dict[str, str]]] = None) -> None:
        if base_prompt is None:
            base_prompt = deepcopy(FACT_CHECKER_PROMPT)
        self.base_prompt = base_prompt

    def __call__(self, claim: str, evidence: str) -> Union[str, List[Dict[str, str]]]:
        prompt = deepcopy(self.base_prompt)
        if isinstance(prompt, str):
            return prompt.format(claim=claim, evidence=evidence)
        item = prompt[-1]
        if isinstance(item, dict):
            item["content"] = item["content"].format(claim=claim, evidence=evidence)
        else:
            raise ValueError("The last item in the prompt list must be a dictionary.")
        return prompt


def build_fact_check_model() -> FactCheckerPipeline:
    raise NotImplementedError("The build_fact_check_model function is not yet implemented.")
