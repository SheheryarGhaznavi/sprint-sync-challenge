from typing import Annotated
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from jose import jwt, JWTError
from sqlalchemy.ext.asyncio import AsyncSession
from sqlmodel import select

from app.core.database import getDBSession
from app.config.token import getToken
from app.models.user import User


oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth/login")



async def getCurrentUser( token: Annotated[str, Depends(oauth2_scheme)], session: Annotated[AsyncSession, Depends(getDBSession)] ) -> User:

    token_settings = getToken()
    status_code = status.HTTP_401_UNAUTHORIZED
    detail = "Could not validate credentials"
    headers = {"WWW-Authenticate": "Bearer"}

    credentials_exception = HTTPException( status_code=status_code, detail=detail, headers=headers )

    try:
        payload = jwt.decode(token, token_settings.jwt_secret, algorithms=[token_settings.jwt_algorithm])
        sub = payload.get("sub")

        if sub is None:
            raise credentials_exception

        user_id = int(sub)

    except (JWTError, ValueError):
        raise credentials_exception

    result = await session.execute(select(User).where(User.id == user_id))
    user = result.scalar_one_or_none()

    if not user:
        raise credentials_exception

    return user




async def getCurrentAdmin(user: Annotated[User, Depends(getCurrentUser)]) -> User:

    if not user.is_admin:
        raise HTTPException(status_code=403, detail="Admin privileges required")

    return user

