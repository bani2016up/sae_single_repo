from pydantic import BaseModel

from typing import Optional, TypeVar


class BaseConfig(BaseModel):

    class Config:
        from_attributes = True


T = TypeVar('T', bound=BaseConfig)

class BaseResponse[T](BaseConfig):
    status: int = 200
    message: str = "Success"
    data: Optional[T] = None
