from typing import Optional
from sqlmodel import SQLModel, Field
import re


class User(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    email: str = Field(index=True, unique=True, max_length=50)
    hashed_password: str = Field(max_length=50)
    is_admin: bool = Field(default=False)

