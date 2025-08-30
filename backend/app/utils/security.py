from datetime import datetime, timedelta, timezone
from typing import Optional
from jose import jwt
from passlib.context import CryptContext

from app.config.token import getToken

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def hashPassword(password: str) -> str:
    return pwd_context.hash(password)



def verifyPassword(plain_password: str, hashed_password: str) -> bool:
    return pwd_context.verify(plain_password, hashed_password)



def createAccessToken(subject: str, expires_minutes: Optional[int] = None) -> str:
    settings = getToken()
    expire = datetime.now(timezone.utc) + timedelta(minutes=expires_minutes or settings.jwt_expires_minutes)
    to_encode = {"sub": subject, "exp": expire}
    return jwt.encode(to_encode, settings.jwt_secret, algorithm=settings.jwt_algorithm)