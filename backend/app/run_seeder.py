import asyncio
import sys
import os

path = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(path)

from app.core.database import async_session_factory
from app.seeds.dev_seed import runDevSeed

# it can be run through this command cd backend && python3 backend/app/run_seeder.py
async def main():

    async with async_session_factory() as session:
        result = await runDevSeed(session)
        print("Seeder completed:", result)


if __name__ == "__main__":
    asyncio.run(main())