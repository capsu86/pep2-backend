from fastapi import APIRouter, Depends
from typing import List
from app.models.user import User
from app.interfaces.user_service_interface import IUserService
from app.services.user_service import UserService
from app.repositories.user_repository import InMemoryUserRepository

router = APIRouter()

# One shared repo & service instance
_user_repo_instance = InMemoryUserRepository()
_user_service_instance = UserService(_user_repo_instance)

def get_user_service() -> IUserService:
    return _user_service_instance

@router.post("/users")
def create_user(user: User, service: IUserService = Depends(get_user_service)):
    service.create_user(user)
    return {"message": "User created successfully"}

@router.get("/users", response_model=List[User])
def list_users(service: IUserService = Depends(get_user_service)):
    return service.list_users()
