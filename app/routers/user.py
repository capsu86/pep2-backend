# app/routers/user.py

import logging
from typing import List

from fastapi import APIRouter, HTTPException, Depends, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from jose import JWTError, jwt
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.user import User, UserCreate
from app.models.user_orm import UserORM
from app.services.user_service import UserService
from app.repositories.user_repository import UserRepository
from app.database import get_session
from app.exceptions.http_exceptions import DuplicateUserException, UserNotFoundException
from app.core.config import SECRET_KEY, ALGORITHM

# ─── Router Setup ────────────────────────────────────────────────────────────
router = APIRouter(prefix="/users", tags=["users"])
logger = logging.getLogger(__name__)

# ─── JWT Config ──────────────────────────────────────────────────────────────
http_bearer = HTTPBearer()

# ─── Dependencies ────────────────────────────────────────────────────────────
def get_user_service(session: AsyncSession = Depends(get_session)):
    repo = UserRepository(session)
    service = UserService(repo)
    return service

async def get_current_user(
    credentials: HTTPAuthorizationCredentials = Depends(http_bearer),
    session: AsyncSession = Depends(get_session)
) -> UserORM:
    token = credentials.credentials
    logger.debug(f"Received token: {token}")
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Invalid authentication credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        logger.debug(f"Decoded JWT payload: {payload}")
        sub = payload.get("sub")
        if sub is None:
            logger.error("JWT payload missing 'sub'")
            raise credentials_exception
        user_id = int(sub)
    except Exception as exc:
        logger.error(f"JWT decode error: {exc}")
        raise credentials_exception

    user_repo = UserRepository(session)
    user = await user_repo.get_by_id(user_id)
    if not user:
        raise credentials_exception
    return user

# ─── Endpoints ───────────────────────────────────────────────────────────────
@router.post("/", response_model=User, status_code=status.HTTP_201_CREATED)
async def create_user(user: UserCreate, service: UserService = Depends(get_user_service)):
    try:
        logger.debug(f"Attempting to create user with email={user.email}")
        created_user = await service.add_user(user)
        if not created_user:
            logger.error(f"User creation failed for email={user.email} without exception")
            raise HTTPException(status_code=400, detail="User could not be created")
        logger.info(f"User created successfully with email={user.email}")
        return created_user
    except DuplicateUserException as dup_exc:
        logger.warning(f"Duplicate user creation attempt for email={user.email}")
        raise dup_exc
    except Exception as exc:
        logger.error(f"Unexpected error creating user with email={user.email}: {exc}", exc_info=True)
        raise HTTPException(status_code=500, detail="Internal server error") from exc

@router.get("/", response_model=List[User])
async def list_users(
    service: UserService = Depends(get_user_service),
    current_user: UserORM = Depends(get_current_user)  # Require authentication
):
    logger.debug("Request to list all users")
    users = await service.get_all_users()
    logger.info(f"Returned {len(users)} users")
    return users

@router.get("/{user_id}", response_model=User)
async def get_user_by_id(
    user_id: int,
    service: UserService = Depends(get_user_service),
    current_user: UserORM = Depends(get_current_user)  # Protejat cu JWT
):
    try:
        logger.debug(f"Fetching user by id={user_id}")
        user = await service.get_user_by_id(user_id)
        logger.info(f"User found with id={user_id}")
        return user
    except UserNotFoundException as not_found_exc:
        logger.warning(f"User not found with id={user_id}")
        raise not_found_exc
    except Exception as exc:
        logger.error(f"Unexpected error fetching user id={user_id}: {exc}", exc_info=True)
        raise HTTPException(status_code=500, detail="Internal server error") from exc
