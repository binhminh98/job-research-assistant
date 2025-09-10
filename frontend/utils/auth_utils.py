"""
Authentication utilities for JWT token management.
"""

from datetime import datetime, timedelta
from pathlib import Path
from typing import Any, Dict, Optional

import bcrypt
import jwt
from config import ALGORITHM, EXPIRATION_MINUTES, SECRET_KEY
from utils.backend_api_client import BackendApiClient
from utils.logging import get_logger

BACKEND_API_CLIENT = BackendApiClient()

file_logger = get_logger(
    "file_" + __name__,
    write_to_file=True,
    log_filepath=Path(r"logs/frontend/auth_utils.log"),
)

stream_logger = get_logger(
    "stream_" + __name__,
)


class JWTTokenAuthUtils:
    def __init__(self):
        self.secret_key = SECRET_KEY
        self.algorithm = ALGORITHM
        self.expiration_minutes = (
            int(EXPIRATION_MINUTES) if EXPIRATION_MINUTES else 30
        )

    def generate_jwt_token(self, username: str, email: str) -> str:
        """
        Generate a JWT token for the given username and email.
        """
        payload = {
            "username": username,
            "email": email,
            "exp": datetime.now() + timedelta(minutes=self.expiration_minutes),
        }

        return jwt.encode(payload, self.secret_key, algorithm=self.algorithm)

    def verify_jwt_token(self, token: str) -> Optional[Dict[str, Any]]:
        """
        Verify a JWT token and return the payload.
        """
        try:
            return jwt.decode(
                token, self.secret_key, algorithms=[self.algorithm]
            )

        except jwt.ExpiredSignatureError:
            file_logger.error(f"JWT token expired!")
            stream_logger.error(f"JWT token expired!")
            return None

        except jwt.InvalidTokenError:
            file_logger.error(f"Invalid JWT token!")
            stream_logger.error(f"Invalid JWT token!")
            return None

    def refresh_jwt_token(self, token: str) -> Optional[str]:
        """
        Refresh a JWT token and return the new token.
        """
        payload = self.verify_jwt_token(token)

        if payload:
            return self.generate_jwt_token(
                payload["username"], payload["email"]
            )

        return None

    def verify_password(self, password: str, hashed_password: str) -> bool:
        """Verify a password against a hashed password."""
        return bcrypt.checkpw(
            password.encode("utf-8"), hashed_password.encode("utf-8")
        )

    def authenticate_user(
        self, login_input: str, password: str
    ) -> Optional[Dict[str, Any]]:
        """Authenticate user against PostgreSQL database."""
        user_response = BACKEND_API_CLIENT.get_user_by_username(login_input)

        user_data = (
            user_response.get("data", {})
            if user_response and user_response.get("success")
            else {}
        )

        if not user_data:
            user_response = BACKEND_API_CLIENT.get_user_by_email(login_input)
            user_data = (
                user_response.get("data", {})
                if user_response and user_response.get("success")
                else {}
            )

        if user_data and self.verify_password(
            password, user_data.get("hashed_password", "")
        ):
            return user_data

        return None


if __name__ == "__main__":
    auth_utils = JWTTokenAuthUtils()
    print(auth_utils.authenticate_user("mlai18", "binhminh98"))
