from os import getenv
from typing import Any, Final, Optional, TypeVar, Callable

from dotenv import load_dotenv


load_dotenv()

T = TypeVar("T")


def get_env(env_variable: str, strict_type: Callable[[str], T] = lambda x: x) -> T:
    if env_value := getenv(env_variable):
        return strict_type(env_value)
    raise ValueError(
        f"{env_variable} does not exist or its value is not set in the .env file"
    )


SUPABASE_URL: Final[str] = get_env("SUPABASE_URL")
SUPABASE_KEY: Final[str] = get_env("SUPABASE_KEY")
JWT_ALGORITHM: Final[str] = get_env("JWT_ALGORITHM")
JWT_SECRET: Final[str] = get_env("JWT_SECRET")
PORT: Final[int] = get_env("PORT", int)
HOST: Final[str] = get_env("HOST")

DEV_MODE: Final[bool] = getenv("DEV_MODE", bool)  # bool(None) == False

ACCESS_TOKEN_MAX_AGE: Final[int] = 60 * 60  # 1 hour in seconds [SUPABASE CONST]
REFRESH_TOKEN_MAX_AGE: Final[int] = (
    30 * 24 * 60 * 60
)  # 30 days in seconds [SUPABASE CONST]
ACCESS_TOKEN: Final[str] = "access_token"
REFRESH_TOKEN: Final[str] = "refresh_token"

AUTO_REFRESH_LOG_LEVEL: Final[str] = get_env("AUTO_REFRESH_LOG_LEVEL")
SERVICES_LOG_LEVEL: Final[str] = get_env("SERVICES_LOG_LEVEL")
