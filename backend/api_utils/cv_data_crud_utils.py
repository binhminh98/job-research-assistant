"""
Module to specify backend logic for the services for CV data CRUD endpoints for job research assistant app.
"""

from pathlib import Path

from db_connectors.postgres.postgres_client import PostgresClient
from general_utils.logging import get_logger
from general_utils.utils import serialize_for_json

POSTGRES_CLIENT = PostgresClient()

file_logger = get_logger(
    "file_" + __name__,
    write_to_file=True,
    log_filepath=Path(r"logs/backend/cv_data_crud_utils.log"),
)


stream_logger = get_logger(
    "stream_" + __name__,
)


class CVDataCrudApiUtils:
    @staticmethod
    def get_cv_data_by_username(username: str) -> list[dict] | None:
        try:
            query = """
                SELECT cd.*, u.username, u.email
                FROM cv_data cd JOIN users u ON cd.user_id = u.id
                WHERE u.username = :username;
            """

            result = POSTGRES_CLIENT.query_db(query, {"username": username})

            if result:
                rows = result.fetchall()
                if rows:
                    return [serialize_for_json(row._asdict()) for row in rows]
            return None

        except Exception as e:
            file_logger.error(
                f"Database error getting CV data by username: {e}"
            )
            stream_logger.error(
                f"Database error getting CV data by username: {e}"
            )
            return None

    @staticmethod
    def get_cv_data_by_file_hash(file_hash: str) -> dict | None:
        try:
            query = """
                    SELECT * FROM cv_data WHERE file_hash = :file_hash
                """

            result = POSTGRES_CLIENT.query_db(query, {"file_hash": file_hash})

            if result:
                row = result.fetchone()
                if row:
                    return serialize_for_json(row._asdict())

            return None

        except Exception as e:
            file_logger.error(
                f"Database error getting CV data by file hash: {e}"
            )
            stream_logger.error(
                f"Database error getting CV data by file hash: {e}"
            )
            return None
