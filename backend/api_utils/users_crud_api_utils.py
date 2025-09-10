"""
Module to specify backend logic for the services for users CRUD endpoints for job research assistant app.
"""

from pathlib import Path

from db_connectors.postgres.postgres_client import PostgresClient
from general_utils.logging import get_logger

POSTGRES_CLIENT = PostgresClient()

file_logger = get_logger(
    "file_" + __name__,
    write_to_file=True,
    log_filepath=Path(r"logs/backend/users_crud_api_utils.log"),
)

stream_logger = get_logger(
    "stream_" + __name__,
)


class UsersCrudApiUtils:
    @staticmethod
    def get_users() -> list[dict] | None:
        try:
            query = """
                SELECT id, username, email
                FROM users
            """
            result = POSTGRES_CLIENT.query_db(query)

            if result:
                rows = result.fetchall()
                if rows:
                    return [row._asdict() for row in rows]
            return None

        except Exception as e:
            file_logger.error(f"Database error getting users: {e}")
            stream_logger.error(f"Database error getting users: {e}")
            return None

    @staticmethod
    def create_user(user: dict) -> dict | None:
        try:
            reg_username_input = user["username"]
            reg_email_input = user["email"]
            reg_password_input = user["password"].get_secret_value()

            user_data = POSTGRES_CLIENT.create_user(
                reg_username_input, reg_email_input, reg_password_input
            )

            if user_data.get("message") == "User created successfully!":
                return {
                    "id": user_data["id"],
                    "username": user_data["username"],
                    "email": user_data["email"],
                    "message": "User created successfully!",
                }
            else:
                return user_data

        except Exception as e:
            file_logger.error(f"Database error creating user: {e}")
            stream_logger.error(f"Database error creating user: {e}")
            return None

    @staticmethod
    def get_user_by_username(username: str) -> dict | None:
        return POSTGRES_CLIENT.get_user_by_username(username)

    @staticmethod
    def get_user_by_email(email: str) -> dict | None:
        return POSTGRES_CLIENT.get_user_by_email(email)
