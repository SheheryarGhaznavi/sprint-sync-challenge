from typing import Optional
from sqlmodel import SQLModel, Field

from app.models.task import TaskStatus


class TaskRequest(SQLModel):
    title: str = Field(max_length=120)
    description: Optional[str] = Field(default="", max_length=4000)
    status: Optional[int] = Field(default=TaskStatus.todo)
    total_minutes: Optional[int] = Field(default=0, ge=0)