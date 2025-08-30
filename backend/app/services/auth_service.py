from typing import Optional
from fastapi import Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlmodel import select

from app.core.database import getDBSession
from app.models.user import User
from app.utils.security import verifyPassword, createAccessToken
from app.services.base_service import BaseService


class AuthService(BaseService):


    def __init__(self, session: AsyncSession = Depends(getDBSession)):
        self.session = session



    async def login(self, form) -> Optional[dict]:

        email = form.username
        password = form.password
        result = await self.session.execute(select(User).where(User.email == email))
        user = result.scalar_one_or_none()

        if not user:
            raise HTTPException(status_code=400, detail="Incorrect email or password")

        if not verifyPassword(password, user.hashed_password):
            raise HTTPException(status_code=400, detail="Incorrect email or password")

        token = createAccessToken(str(user.id))

        return {
            "access_token": token,
            "token_type": "bearer",
            "user": {"id": user.id, "email": user.email, "is_admin": user.is_admin},
        }

