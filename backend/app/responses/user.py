from sqlmodel import SQLModel
from typing import List


class UserRead(SQLModel):
    id: int
    email: str
    is_admin: bool
    
    
class UsersListResponse(SQLModel):
    error: int
    message: str
    data: List[UserRead]

