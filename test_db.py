# test_db.py
import asyncio
from app.database import engine, Base

async def init_db():
    # Create all tables in the DB (no-op if they already exist)
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    print("✅ Tables created (or already exist)")

if __name__ == "__main__":
    asyncio.run(init_db())
