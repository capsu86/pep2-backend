from app.interfaces.user_interface import IUserService
from app.models.user import User
from typing import List

# Simple memory-based service (for dev or testing)
class InMemoryUserService(IUserService):
    def __init__(self):
        self._users = []

    def add_user(self, user: User) -> User:
        # Simulate a uniqueness check
        if any(u.email == user.email for u in self._users):
            raise ValueError("User with this email already exists.")
        self._users.append(user)
        return user

    def get_all_users(self) -> List[User]:
        return self._users
