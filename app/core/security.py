# app/core/security.py
from passlib.context import CryptContext

# Password hashing context setup using bcrypt
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def hash_password(password: str) -> str:
    """
    Hashes the plain password using bcrypt algorithm.
    This function is used to securely store passwords.
    """
    return pwd_context.hash(password)

def verify_password(plain_password: str, hashed_password: str) -> bool:
    """
    Verifies a plain password against the hashed password.
    Returns True if passwords match, False otherwise.
    """
    return pwd_context.verify(plain_password, hashed_password)
