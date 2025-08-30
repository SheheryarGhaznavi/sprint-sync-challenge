from sqlmodel import SQLModel
from typing import List, Union


class UserRead(SQLModel):
    id: int
    email: str
    is_admin: bool



class UsersListResponse(SQLModel):
    error: int
    message: str
    data: List[UserRead]



class UserResponse(SQLModel):
    error: int
    message: str
    data: Union[UserRead, List] = []

