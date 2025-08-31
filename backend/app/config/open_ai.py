from functools import lru_cache
from pydantic_settings import BaseSettings
from pydantic import Field
import os


class OpenAI(BaseSettings):

    # OpenAI
    openai_api_key: str | None = Field(default=None)
    openai_model: str = Field(default="gpt-4o-mini")

    class Config:
        env_file = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(__file__))), ".env")
        case_sensitive = False
        extra = 'ignore'

@lru_cache
def getOpenAI() -> OpenAI:
    return OpenAI()  # type: ignore

