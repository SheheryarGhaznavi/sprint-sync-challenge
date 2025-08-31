from typing import Optional
from enum import Enum
from sqlmodel import SQLModel, Field



class TaskStatus(Enum):
    todo = 1
    in_progress = 2
    done = 3



class Task(SQLModel, table=True):

    __tablename__ = "tasks"

    id: Optional[int] = Field(default=None, primary_key=True)
    title: str = Field(max_length=120, index=True)
    description: str = Field(default="", max_length=4000)
    status: int = Field(default=TaskStatus.todo)
    total_minutes: int = Field(default=0, ge=0)
    user_id: int = Field(index=True, foreign_key="users.id")