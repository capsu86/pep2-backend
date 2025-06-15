"""
Core configuration module for the application.
"""
import os

# JWT Settings
SECRET_KEY = os.getenv("SECRET_KEY", "your-very-secret-key")  # Default secret key if not in env
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 60  # 1 hour expiration
