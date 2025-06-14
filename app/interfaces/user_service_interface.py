from abc import ABC, abstractmethod
from typing import List
from app.models.user import User

# This interface defines what the UserService must implement
class IUserService(ABC):
    @abstractmethod
    def create_user(self, user: User) -> None:
        pass

    @abstractmethod
    def list_users(self) -> List[User]:
        pass
