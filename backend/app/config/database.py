from functools import lru_cache
from pydantic_settings import BaseSettings
from pydantic import Field
import os


class DB(BaseSettings):

    # Database
    db_host: str = Field(default="db")
    db_port: int = Field(default=3306)
    db_user: str = Field(default="sprintsync")
    db_password: str = Field(default="sprintsync")
    db_name: str = Field(default="sprintsync")

    class Config:
        env_file = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(__file__))), ".env")
        case_sensitive = False
        extra='ignore'

@lru_cache
def getDB():
    return DB()