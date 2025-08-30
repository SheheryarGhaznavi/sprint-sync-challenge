from typing import List
from sqlalchemy.ext.asyncio import AsyncSession
from sqlmodel import select
from app.core.database import getDBSession
from fastapi import Depends
from app.models.user import User


class UserService:
    def __init__(self, session: AsyncSession = Depends(getDBSession)):
        self.session = session

    async def list(self, skip: int = 0, limit: int = 50) -> List[User]:
        result = await self.session.execute(select(User).offset(skip).limit(limit))
        return list(result.scalars().all())