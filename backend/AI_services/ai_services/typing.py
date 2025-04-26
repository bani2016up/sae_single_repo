from typing import (
    TypeAlias,
    Dict,
    List,
    Literal,
    Union,
    Callable,
    Any
)

from .interfaces import PromptInterface

__all__ = (
    "DeviceType",
    "DocumentMetadataType",
    "PromptType",
    "PromptGeneratorType",
)

DeviceType: TypeAlias = Literal["cpu", "cuda"]
DocumentMetadataType: TypeAlias = Dict[str, Any]

PromptType: TypeAlias = Union[str, List[Dict[str, str]]]
PromptGeneratorType: TypeAlias = Union[PromptInterface, Callable[..., PromptType]]
