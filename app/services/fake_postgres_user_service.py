from app.interfaces.user_interface import IUserService
from app.models.user import User
from typing import List

# Fake implementation that simulates interaction with a database
class FakePostgresUserService(IUserService):
    def __init__(self):
        self._db_sim = {}

    def add_user(self, user: User) -> User:
        if user.email in self._db_sim:
            raise ValueError("User already in DB.")
        self._db_sim[user.email] = user
        return user

    def get_all_users(self) -> List[User]:
        return list(self._db_sim.values())
