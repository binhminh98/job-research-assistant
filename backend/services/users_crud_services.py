"""
Module to specify services for the users CRUD endpoints for job research assistant app.
"""

from api_utils.users_crud_api_utils import UsersCrudApiUtils


class UsersServices:
    @staticmethod
    def get_users() -> list[dict] | None:
        return UsersCrudApiUtils.get_users()

    @staticmethod
    def create_user(user: dict) -> dict | None:
        return UsersCrudApiUtils.create_user(user)

    @staticmethod
    def get_user_by_username(username: str) -> dict | None:
        return UsersCrudApiUtils.get_user_by_username(username)

    @staticmethod
    def get_user_by_email(email: str) -> dict | None:
        return UsersCrudApiUtils.get_user_by_email(email)
