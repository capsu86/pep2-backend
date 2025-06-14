import sys, os
sys.path.append(os.path.dirname(os.path.dirname(__file__)))

import pytest
from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker
from app.database import Base
from app.repositories.user_repository import UserRepository
from app.services.user_service import UserService

DATABASE_URL = "sqlite+aiosqlite:///:memory:"

@pytest.fixture(scope="session")
async def engine():
    engine = create_async_engine(DATABASE_URL, echo=False)
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    yield engine
    await engine.dispose()

@pytest.fixture
async def session(engine):
    async_session = async_sessionmaker(bind=engine, class_=type((await engine.begin()).run_sync(lambda c: None).__class__), expire_on_commit=False)
    async with async_session() as session:
        yield session

@pytest.fixture
async def user_repository(session):
    return UserRepository(session)

@pytest.fixture
async def user_service(user_repository):
    return UserService(user_repository)
