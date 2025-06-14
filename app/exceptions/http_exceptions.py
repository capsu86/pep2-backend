# app/exceptions/http_exceptions.py
from fastapi import HTTPException, status

class DuplicateUserException(HTTPException):
    def __init__(self):
        super().__init__(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="User with same email already exists."
        )

class UserNotFoundException(HTTPException):
    def __init__(self):
        super().__init__(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found."
        )
