# app/database.py

from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine, async_sessionmaker
from sqlalchemy.orm import declarative_base
import os

# ─── Database Configuration ─────────────────────────────────────────────────

# Read the DATABASE_URL env var, fallback to local Postgres:
DATABASE_URL = os.getenv(
    "DATABASE_URL",
    "postgresql+asyncpg://pepuser:pepuser@localhost:5432/pep2"
)

# Create the async SQLAlchemy engine; echo=True logs SQL to console
engine = create_async_engine(DATABASE_URL, echo=True)

# Session factory for dependency injection (each request gets its own session)
async_session_factory = async_sessionmaker(
    bind=engine,
    class_=AsyncSession,
    expire_on_commit=False  # keep attributes after commit for readback
)

# Base class for all ORM models
Base = declarative_base()

# Dependency that yields a DB session, automatically opened & closed per request
async def get_session() -> AsyncSession:
    async with async_session_factory() as session:
        yield session
