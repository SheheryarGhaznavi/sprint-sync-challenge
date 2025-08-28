from functools import lru_cache
from pydantic_settings import BaseSettings
from pydantic import Field


class Token(BaseSettings):

    # Security
    jwt_secret: str = Field(default="changeme")
    jwt_algorithm: str = Field(default="HS256")
    jwt_expires_minutes: int = Field(default=60)

@lru_cache
def getToken() -> Token:
    return Token()  # type: ignore




