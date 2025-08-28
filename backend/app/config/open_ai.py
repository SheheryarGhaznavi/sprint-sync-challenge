from functools import lru_cache
from pydantic_settings import BaseSettings
from pydantic import Field


class OpenAI(BaseSettings):

    # OpenAI
    openai_api_key: str | None = None
    openai_model: str = Field(default="gpt-4o-mini")

@lru_cache
def getOpenAI() -> OpenAI:
    return OpenAI()  # type: ignore

