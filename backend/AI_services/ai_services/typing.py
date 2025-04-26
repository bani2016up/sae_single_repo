from typing import (
    TypeAlias,
    Dict,
    List,
    Literal,
    Union,
    Any
)

__all__ = (
    "DeviceType",
    "DocumentMetadataType",
    "PromptType",
)

DeviceType: TypeAlias = Literal["cpu", "cuda"]
DocumentMetadataType: TypeAlias = Dict[str, Any]

PromptType: TypeAlias = Union[str, List[Dict[str, str]]]