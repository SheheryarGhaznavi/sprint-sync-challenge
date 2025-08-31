from typing import List, Optional
from sqlalchemy.ext.asyncio import AsyncSession
from sqlmodel import select
from fastapi import Depends, HTTPException

from app.core.database import getDBSession
from app.models.task import Task, TaskStatus
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



    async def getById(self, user: User, task_id: int) -> Optional[Task]:

        if not user.is_admin:
            result = await self.session.execute(select(Task).where(Task.id == task_id))
        else:
            result = await self.session.execute(select(Task).where(Task.id == task_id).where(Task.user_id == user.id))
        return result.scalar_one_or_none()



    async def update(self, user: User, task_id: int, task_data: Task) -> Task:
        task = await self.getById(user, task_id)
        
        if not task:
            raise HTTPException(status_code = 404, detail = "Task not found")
        
        task.title = task_data.title
        task.description = task_data.description
        task.status = task_data.status
        task.total_minutes = task_data.total_minutes
        await self.session.commit()
        await self.session.refresh(task)
        return task



    async def delete(self, user: User, task_id: int) -> None:
        task = await self.getById(user, task_id)

        if not task:
            raise HTTPException(status_code = 404, detail = "Task not found")

        await self.session.delete(task)
        await self.session.commit()



    async def updateStatus(self, user: User, task_id: int, status: int) -> Task:
        task = await self.getById(user, task_id)

        if not task:
            raise HTTPException(status_code = 404, detail = "Task not found")
        
        if task.status == TaskStatus.done.value:
            raise HTTPException(status_code = 400, detail = "Task is already done")

        task.status = status
        await self.session.commit()
        await self.session.refresh(task)
        return task