from sqlalchemy.ext.asyncio import AsyncSession
from sqlmodel import select

from app.models.user import User
from app.models.task import Task
from app.utils.security import hashPassword


async def runDevSeed(session: AsyncSession) -> dict:
    created = {"user": False, "tasks": 0}

    # Admin user
    email = "admin@gmail.com"
    password = "admin123"
    
    result = await session.execute(select(User).where(User.email == email))
    admin = result.scalar_one_or_none()
    
    if not admin:
        admin = User(email=email, hashed_password=hashPassword(password), is_admin=True)
        session.add(admin)
        await session.commit()
        await session.refresh(admin)
        created["user"] = True

    # Demo tasks
    result = await session.execute(select(Task).where(Task.user_id == admin.id))
    tasks = list(result.scalars().all())
    
    if not tasks:
    
        demo = [
            Task(title="Setup project skeleton", description="Initialize backend and frontend", status=1, user_id=admin.id),
            Task(title="Implement auth", description="JWT login and guards", status=1, user_id=admin.id),
            Task(title="Task CRUD", description="Create, list, update, delete tasks", status=1, user_id=admin.id),
        ]
    
        for t in demo:
            session.add(t)
    
        await session.commit()
        created["tasks"] = len(demo)

    return created

