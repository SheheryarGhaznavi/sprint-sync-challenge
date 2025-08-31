from typing import List
from sqlalchemy.ext.asyncio import AsyncSession
from sqlmodel import select
from fastapi import Depends

from app.core.database import getDBSession
from app.models.task import Task
from app.models.user import User
from app.services.base_service import BaseService


class TaskService(BaseService):


    def __init__(self, session: AsyncSession = Depends(getDBSession)):
        self.session = session



    async def list(self, user: User, skip: int = 0, limit: int = 50) -> List[Task]:

        if not user.is_admin:
            result = await self.session.execute(select(Task).offset(skip).limit(limit))
        else:
            result = await self.session.execute(select(Task).where(Task.user_id == user.id).offset(skip).limit(limit))
        
        return list(result.scalars().all())
    


    async def create(self, user: User, task: Task) -> Task:

        task = Task(
            title = task.title,
            description = task.description or "",
            status = task.status,
            total_minutes = task.total_minutes or 0,
            user_id = user.id,
        )

        self.session.add(task)
        await self.session.commit()
        await self.session.refresh(task)
        return task