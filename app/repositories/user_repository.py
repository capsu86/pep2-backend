# app/repositories/user_repository.py
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from app.models.user_orm import UserORM

class UserRepository:
    def __init__(self, session: AsyncSession):
        self.session = session

    async def add(self, user_orm: UserORM) -> UserORM:
        self.session.add(user_orm)
        await self.session.commit()
        await self.session.refresh(user_orm)
        return user_orm

    async def get_all(self) -> list[UserORM]:
        result = await self.session.execute(select(UserORM))
        return result.scalars().all()

    async def get_by_id(self, user_id: int) -> UserORM | None:
        result = await self.session.execute(select(UserORM).where(UserORM.id == user_id))
        return result.scalars().first()

    async def get_by_email(self, email: str) -> UserORM | None:
        result = await self.session.execute(select(UserORM).where(UserORM.email == email))
        return result.scalars().first()

    async def create_access_token(self, user: UserORM) -> str:
        access_token = auth_service.create_access_token(data={"sub": str(user.id)})
        return Token(access_token=access_token)
