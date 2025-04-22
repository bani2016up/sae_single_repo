

from core.pydantic import BaseConfig


class ProjectResponse(BaseConfig):
    id: int
    title: str

class ProjectGoal(BaseConfig):
    id: int
    content: str
    is_reached: bool

class ProjectSourceLink(BaseConfig):
    id: int
    title: str
    url: str
