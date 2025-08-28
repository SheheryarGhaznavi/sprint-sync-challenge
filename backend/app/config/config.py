from functools import lru_cache
from pydantic_settings import BaseSettings
from pydantic import Field


class Config(BaseSettings):
    app_name: str = "SprintSync API"
    environment: str = Field(default="development")
    env_file = ".env"
    case_sensitive = False

@lru_cache
def getConfigs() -> Config:
    return Config()  # type: ignore

