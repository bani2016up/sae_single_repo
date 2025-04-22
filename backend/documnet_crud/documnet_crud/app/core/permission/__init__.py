from typing import NoReturn, Optional
from database.database.database import AsyncSession
from fastapi.exceptions import HTTPException


def check_access_to_document(
    project_id: int,
    user_id: int,
    sess: AsyncSession,
    raises: Optional[HTTPException] = HTTPException(403, "Access denied to this project."),
) -> None | NoReturn: ...
