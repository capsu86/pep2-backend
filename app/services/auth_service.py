# app/services/auth_service.py
import jwt
from datetime import datetime, timedelta
from app.core.password_hashing import verify_password, hash_password
from app.models.user import User
from app.repositories.user_repository import UserRepository
from app.exceptions.http_exceptions import UserNotFoundException
from app.models.token import TokenPayload
from app.core.config import SECRET_KEY, ALGORITHM, ACCESS_TOKEN_EXPIRE_MINUTES

class AuthService:
    def __init__(self, user_repository: UserRepository):
        self.user_repository = user_repository

    def verify_password(self, plain_password: str, hashed_password: str) -> bool:
        """
        Verify plain password against hashed password.
        """
        return verify_password(plain_password, hashed_password)

    def hash_password(self, password: str) -> str:
        """
        Hash plain password using bcrypt.
        """
        return hash_password(password)

    async def authenticate_user(self, email: str, password: str) -> User | None:
        """
        Verify user credentials:
        - fetch user by email
        - verify password
        Returns User if valid, else None.
        """
        user_orm = await self.user_repository.get_by_email(email)
        if not user_orm:
            return None
        try:
            if not self.verify_password(password, user_orm.hashed_password):
                return None
        except Exception:
            # If hash is invalid or any error occurs, treat as invalid credentials
            return None
        return User.from_orm(user_orm)

    def create_access_token(self, data: dict, expires_delta: timedelta | None = None) -> str:
        """
        Create a JWT access token with payload data and expiry.
        """
        to_encode = data.copy()
        expire = datetime.utcnow() + (expires_delta or timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES))
        to_encode.update({"exp": expire})
        encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
        return encoded_jwt

    def decode_access_token(self, token: str) -> TokenPayload | None:
        """
        Decode JWT token to TokenPayload.
        Returns None if invalid or expired.
        """
        try:
            payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
            token_data = TokenPayload(**payload)
            return token_data
        except jwt.PyJWTError:
            return None
