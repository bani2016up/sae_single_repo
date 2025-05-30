import os


origins: list[str] = os.getenv("API_ORIGINS").split(",") if os.getenv("API_ORIGINS") else ["*"]  # type: ignore
methods: list[str] = ["GET", "POST", "PUT", "DELETE", "OPTIONS", "PATCH"]
headers: list[str] = ["*"]
allow_credentials: bool = True
max_age: int = 3600
