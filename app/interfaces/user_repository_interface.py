from abc import ABC, abstractmethod
from typing import List
from app.models.user import User

class IUserRepository(ABC):
    @abstractmethod
    def add_user(self, user: User) -> None:
        pass

    @abstractmethod
    def get_all_users(self) -> List[User]:
        pass
