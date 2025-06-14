# app/routers/user.py
import logging
from fastapi import APIRouter, HTTPException, Depends, status
from typing import List
from app.models.user import User
from app.services.user_service import UserService
from app.repositories.user_repository import UserRepository
from app.database import get_session
from sqlalchemy.ext.asyncio import AsyncSession
from app.exceptions.http_exceptions import DuplicateUserException, UserNotFoundException

router = APIRouter(prefix="/users", tags=["users"])

logger = logging.getLogger(__name__)  # Logger for this router module

def get_user_service(session: AsyncSession = Depends(get_session)):
    # Create repository and service instances per request
    repo = UserRepository(session)
    service = UserService(repo)
    return service

@router.post("/", response_model=User, status_code=status.HTTP_201_CREATED)
async def create_user(user: User, service: UserService = Depends(get_user_service)):
    """
    Endpoint to create a new user.
    Raises HTTP 400 if user could not be created (e.g., duplicate email).
    """
    try:
        logger.debug(f"Attempting to create user with email={user.email}")
        created_user = await service.add_user(user)
        if not created_user:
            # Defensive fallback, should not normally happen if no exception raised
            logger.error(f"User creation failed for email={user.email} without exception")
            raise HTTPException(status_code=400, detail="User could not be created")
        logger.info(f"User created successfully with email={user.email}")
        return created_user

    except DuplicateUserException as dup_exc:
        logger.warning(f"Duplicate user creation attempt for email={user.email}")
        raise dup_exc  # Pass through to return HTTP 400 with proper message

    except Exception as exc:
        logger.error(f"Unexpected error creating user with email={user.email}: {exc}", exc_info=True)
        # Generic error handling to avoid leaking internal errors, return HTTP 500
        raise HTTPException(status_code=500, detail="Internal server error") from exc

@router.get("/", response_model=List[User])
async def list_users(service: UserService = Depends(get_user_service)):
    """
    Endpoint to list all users.
    """
    logger.debug("Request to list all users")
    users = await service.get_all_users()
    logger.info(f"Returned {len(users)} users")
    return users

@router.get("/{user_id}", response_model=User)
async def get_user_by_id(user_id: int, service: UserService = Depends(get_user_service)):
    """
    Endpoint to get a user by ID.
    Raises HTTP 404 if user not found.
    """
    try:
        logger.debug(f"Fetching user by id={user_id}")
        user = await service.get_user_by_id(user_id)
        logger.info(f"User found with id={user_id}")
        return user

    except UserNotFoundException as not_found_exc:
        logger.warning(f"User not found with id={user_id}")
        raise not_found_exc  # Return 404 to client

    except Exception as exc:
        logger.error(f"Unexpected error fetching user id={user_id}: {exc}", exc_info=True)
        raise HTTPException(status_code=500, detail="Internal server error") from exc
