from typing import List, Optional
from sqlalchemy.ext.asyncio import AsyncSession
from sqlmodel import select
from app.core.database import getDBSession
from fastapi import Depends, HTTPException
from app.models.user import User
from app.services.base_service import BaseService
from app.utils.security import hashPassword


class UserService(BaseService):


    def __init__(self, session: AsyncSession = Depends(getDBSession)):
        self.session = session



    async def list(self, skip: int = 0, limit: int = 50) -> List[User]:
        result = await self.session.execute(select(User).offset(skip).limit(limit))
        return list(result.scalars().all())
    


    async def create(self, user: User) -> User:
        user = User(email=user.email, hashed_password=hashPassword(user.password), is_admin=user.is_admin)
        self.session.add(user)
        await self.session.commit()
        await self.session.refresh(user)
        return user



    async def getById(self, user_id: int) -> Optional[User]:
        result = await self.session.execute(select(User).where(User.id == user_id))
        return result.scalar_one_or_none()
    


    async def update(self, user_id: int, user_data: User) -> User:
        user = await self.getById(user_id)
        
        if not user:
            raise HTTPException(status_code=404, detail="User not found")
        
        user.email = user_data.email
        user.is_admin = user_data.is_admin
        user.hashed_password = hashPassword(user_data.password)
        await self.session.commit()
        await self.session.refresh(user)
        return user



    async def delete(self, user_id: int) -> None:
        user = await self.getById(user_id)

        if not user:
            raise HTTPException(status_code=404, detail="User not found")

        await self.session.delete(user)
        await self.session.commit()