from sqlmodel import SQLModel, Field


class SuggestRequest(SQLModel):
    title: str = Field(min_length=15, max_length=120)