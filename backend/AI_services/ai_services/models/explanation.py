from transformers import pipeline
from typing import Literal

from ..interfaces import DeviceAwareModel


class ExplanationLLM(DeviceAwareModel):
    def __init__(
        self,
        model: str = "Open-Orca/Mistral-7B-OpenOrca",
        *,
        device: Literal["cuda", "cpu"] = "cuda",
        torch_dtype: str = "auto",
        device_map: str = "auto",
    ) -> None:
        super().__init__(device=device)
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
        max_new_tokens: int = 256,
        do_sample: bool = False,
        temperature: float = 0.1
    ) -> str:
        # FIXME: prompt.
        prompt = f"Claim: {claim}\nEvidence: {evidence}\nExplain why this claim is true or false."
        response = self.llm(
            prompt,
            max_new_tokens=max_new_tokens,
            do_sample=do_sample,
            temperature=temperature
        )
        return response[0]['generated_text']

    forward = __call__
