from sqlmodel import SQLModel
from typing import List, Union


class TaskRead(SQLModel):
    id: int
    title: str
    description: str
    status: int
    total_minutes: int
    user_id: int



class TasksListResponse(SQLModel):
    error: int
    message: str
    data: List[TaskRead]



class TaskResponse(SQLModel):
    error: int
    message: str
    data: Union[TaskRead, List] = []

