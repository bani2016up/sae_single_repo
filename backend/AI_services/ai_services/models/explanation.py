import torch

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
        self._device = device  # will work in feature/ai/fact-checking
        self.llm.tokenizer.to(device)
        self.llm.model.to(device)
