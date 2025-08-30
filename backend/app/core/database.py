from typing import AsyncGenerator
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import sessionmaker

from app.config.database import getDB
db = getDB()

DATABASE_URL = (
    f"mysql+aiomysql://{db.db_user}:{db.db_password}"
    f"@{db.db_host}:{db.db_port}/{db.db_name}"
)

engine = create_async_engine(DATABASE_URL, future=True, echo=True, pool_pre_ping=True)

async_session_factory = sessionmaker(
    engine, class_=AsyncSession, expire_on_commit=False, autoflush=False, autocommit=False
)


async def getDBSession() -> AsyncGenerator[AsyncSession, None]:
    async with async_session_factory() as session:
        yield session

