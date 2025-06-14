from typing import List
from app.models.user import User
from app.interfaces.user_service_interface import IUserService
from app.interfaces.user_repository_interface import IUserRepository

# Concrete implementation of business logic for users
class UserService(IUserService):
    def __init__(self, user_repository: IUserRepository):
        # Inject repository dependency (dependency inversion)
        self._user_repository = user_repository

    def create_user(self, user: User) -> None:
        # Business logic can be added here (e.g., validation, logging)
        self._user_repository.add_user(user)

    def list_users(self) -> List[User]:
        return self._user_repository.get_all_users()
