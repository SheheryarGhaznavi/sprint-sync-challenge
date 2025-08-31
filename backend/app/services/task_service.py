from typing import List
from sqlalchemy.ext.asyncio import AsyncSession
from sqlmodel import select
from app.core.database import getDBSession
from fastapi import Depends
from app.models.task import Task
from app.services.base_service import BaseService


class TaskService(BaseService):


    def __init__(self, session: AsyncSession = Depends(getDBSession)):
        self.session = session



    async def list(self, user: int, skip: int = 0, limit: int = 50) -> List[Task]:

        if not user.is_admin:
            result = await self.session.execute(select(Task).offset(skip).limit(limit))
        else:
            result = await self.session.execute(select(Task).where(Task.user_id == user.id).offset(skip).limit(limit))
        
        return list(result.scalars().all())