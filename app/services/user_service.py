# app/services/user_service.py
import logging
from app.models.user import User
from app.models.user_orm import UserORM
from app.repositories.user_repository import UserRepository
from app.exceptions.http_exceptions import DuplicateUserException, UserNotFoundException

logger = logging.getLogger(__name__)

class UserService:
    def __init__(self, repository: UserRepository):
        self.repository = repository

    async def add_user(self, user: User) -> User:
        logger.debug(f"Checking if user with email={user.email} already exists.")
        existing = await self.repository.get_by_email(user.email)
        if existing:
            logger.error(f"Duplicate user detected with email={user.email}")
            raise DuplicateUserException()

        logger.info(f"Adding new user with email={user.email}")
        user_orm = UserORM(**user.dict(exclude_unset=True))
        user_orm = await self.repository.add(user_orm)
        logger.info(f"User added successfully with id={user_orm.id}")
        return User.from_orm(user_orm)

    async def get_all_users(self) -> list[User]:
        logger.debug("Fetching all users from repository.")
        users_orm = await self.repository.get_all()
        logger.info(f"Fetched {len(users_orm)} users.")
        return [User.from_orm(u) for u in users_orm]

    async def get_user_by_id(self, user_id: int) -> User:
        logger.debug(f"Fetching user with id={user_id}")
        user_orm = await self.repository.get_by_id(user_id)
        if user_orm is None:
            logger.warning(f"User not found with id={user_id}")
            raise UserNotFoundException()
        logger.info(f"User found with id={user_id}")
        return User.from_orm(user_orm)
