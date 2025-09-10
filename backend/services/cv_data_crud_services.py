"""
Module to specify services for the CV data CRUD endpoints for job research assistant app.
"""

from api_utils.cv_data_crud_utils import CVDataCrudApiUtils


class CVDataCrudServices:
    @staticmethod
    def get_cv_data_by_username(username: str) -> list[dict] | None:
        return CVDataCrudApiUtils.get_cv_data_by_username(username)

    @staticmethod
    def get_cv_data_by_file_hash(file_hash: str) -> dict | None:
        return CVDataCrudApiUtils.get_cv_data_by_file_hash(file_hash)
