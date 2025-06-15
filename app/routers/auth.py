# app/routers/auth.py

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from app.models.user import UserLogin
from app.models.token import Token
from app.services.auth_service import AuthService
from app.repositories.user_repository import UserRepository
from app.database import get_session

router = APIRouter(tags=["auth"])

# Dependency injection of AuthService with DB session
async def get_auth_service(session: AsyncSession = Depends(get_session)) -> AuthService:
    user_repo = UserRepository(session)
    return AuthService(user_repo)

@router.post("/login", response_model=Token)
async def login(
    credentials: UserLogin,
    auth_service: AuthService = Depends(get_auth_service)
):
    user = await auth_service.authenticate_user(credentials.email, credentials.password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid email or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token = auth_service.create_access_token(data={"sub": str(user.id)})
    return Token(access_token=access_token, token_type="bearer")
