"""
Module to specify Pydantic models for the users CRUD endpoints.
"""

from pydantic import BaseModel, EmailStr, SecretStr


class UserCreateRequest(BaseModel):
    username: str
    email: EmailStr
    password: SecretStr
