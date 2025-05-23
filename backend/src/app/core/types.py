from .database.connection import AsyncSession
from typing import Final

type idType = int


EXCEPTED_FILE_EXTENSIONS: Final[set[str]] = {".txt", ".rtf"}
