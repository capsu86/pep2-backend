# app/models/user_orm.py

from sqlalchemy import Column, Integer, String
from app.database import Base

class UserORM(Base):
    """
    SQLAlchemy ORM model mapping the 'users' table in Postgres.
    Columns:
      - id: primary key
      - name: non-null text
      - email: unique, indexed text
      - hashed_password: securely stored (bcrypt hash), required for auth
    """
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    email = Column(String, unique=True, index=True)
    hashed_password = Column(String, nullable=False)
