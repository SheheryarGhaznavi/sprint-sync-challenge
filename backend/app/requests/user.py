from sqlmodel import SQLModel, Field
from pydantic import field_validator
import re


class UserRequest(SQLModel):
    email: str = Field(max_length=50)
    password: str = Field(min_length=8, max_length=128)
    is_admin: bool = Field(default=False)

    @field_validator("email")
    @classmethod
    def validateEmailFormat(cls, v: str) -> str:
        if not validateEmail(v):
            raise ValueError("invalid email format")
        return v



EMAIL_REGEX = re.compile(r"^[^@\s]+@[^@\s]+\.[^@\s]+$")


def validateEmail(email: str) -> bool:
    return bool(EMAIL_REGEX.match(email))