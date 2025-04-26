from transformers import pipeline
from typing import Literal, Callable, Union

from ..interfaces import DeviceAwareModel
from ..utils import FactCheckerPrompt
from ..interfaces import PromptInterface


class ExplanationLLM(DeviceAwareModel):
    def __init__(
        self,
        model: str = "Open-Orca/Mistral-7B-OpenOrca",
        *,
        device: Literal["cuda", "cpu"] = "cuda",
        prompt_generator: Union[PromptInterface, Callable] = None,
        torch_dtype: str = "auto",
        device_map: str = "auto",
    ) -> None:
        """
        Initializes the ExplanationLLM model.

        Args:
            model (str): The model name or path.
            device (Literal["cuda", "cpu"]): Target device for model operations.
            prompt_generator (Union[PromptInterface, Callable]): A callable or instance of
                    PromptInterface for generating prompts.
            torch_dtype (str): Data type for the model.
            device_map (str): Device map for the model.
        """
        super().__init__(device=device)
        if prompt_generator is None:
            prompt_generator = FactCheckerPrompt()
        self.prompt_generator = prompt_generator
        self.llm = pipeline(
            "text-generation", model=model,
            torch_dtype=torch_dtype,
            device_map=device_map
        )
        self.llm.tokenizer.to(device)
        self.llm.model.to(device)

    def to(self, device: Literal["cpu", "cuda"]) -> None:
        """
        Transfers the model to the specified device.

        Parameters:
            device (Literal["cpu", "cuda"]): A valid device string.

        Raises:
            ValueError: If the specified device is not supported.

        Examples:
            model.to("cuda")
        """
        self._device = device
        self.llm.tokenizer.to(device)
        self.llm.model.to(device)

    def __call__(
        self, claim: str,
        evidence: str,
        *,
        max_new_tokens: int = 256,
        do_sample: bool = False,
        temperature: float = 0.1
    ) -> str:
        """
        Generates an explanation for the given claim and evidence.

        Args:
            claim (str): The claim to be evaluated.
            evidence (str): The evidence to support or refute the claim.
            max_new_tokens (int): Maximum number of tokens to generate.
            do_sample (bool): Whether to sample from the distribution.
            temperature (float): Sampling temperature.

        Returns:
            str: The generated explanation.
        """
        prompt = self.prompt_generator(claim, evidence)
        response = self.llm(
            prompt,
            max_new_tokens=max_new_tokens,
            do_sample=do_sample,
            temperature=temperature
        )
        return response[0]['generated_text']

    forward = __call__
