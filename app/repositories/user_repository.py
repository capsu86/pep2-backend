from typing import List
from app.models.user import User
from app.interfaces.user_repository_interface import IUserRepository

class InMemoryUserRepository(IUserRepository):
    def __init__(self):
        self._users: List[User] = []

    def add_user(self, user: User) -> None:
        self._users.append(user)

    def get_all_users(self) -> List[User]:
        return self._users
