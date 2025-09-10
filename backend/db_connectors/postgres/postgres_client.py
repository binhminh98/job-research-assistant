"""
Helper module to connect to Postgres and perform operations like querying the database.
"""

import json
from pathlib import Path
from typing import Any, Dict

import bcrypt
from config import (
    POSTGRES_DB,
    POSTGRES_HOST,
    POSTGRES_PASSWORD,
    POSTGRES_PORT,
    POSTGRES_USER,
)
from general_utils.logging import get_logger
from general_utils.utils import serialize_for_json
from langchain_community.vectorstores import PGVector
from sqlalchemy import Result, create_engine, text
from sqlalchemy.orm import sessionmaker

file_logger = get_logger(
    "file_" + __name__,
    write_to_file=True,
    log_filepath=Path(r"logs/postgres/postgres.log"),
)

stream_logger = get_logger(
    "stream_" + __name__,
)

DATABASE_URL = f"postgresql+psycopg2://{POSTGRES_USER}:{POSTGRES_PASSWORD}@{POSTGRES_HOST}:{POSTGRES_PORT}/{POSTGRES_DB}"


class PostgresClient:
    def __init__(self):
        self.engine = self._get_engine()

    def _get_engine(self):
        return create_engine(DATABASE_URL)

    def _get_connection_context(self):
        session_maker = sessionmaker(
            autocommit=False, autoflush=False, bind=self.engine
        )

        return session_maker()

    def query_db(self, query, params=None) -> Result[Any] | None:
        try:
            with self._get_connection_context() as session:
                result = session.execute(text(query), params=params)

                session.commit()

                stream_logger.info(f"Query executed successfully!")
                return result

        except Exception as e:
            file_logger.error(f"Failed to query database: {e}")
            stream_logger.error(f"Failed to query database: {e}")
            raise e

    def get_user_by_username(self, username: str) -> Dict:
        """Get user data by username from database."""
        try:
            query = """
                SELECT id, username, email, hashed_password
                FROM users
                WHERE username = :username
            """
            result = self.query_db(query, {"username": username})

            if result:
                row = result.fetchone()
                if row:
                    return {
                        "id": row[0],
                        "username": row[1],
                        "email": row[2],
                        "hashed_password": row[3],
                        "message": "User found!",
                    }
            return {"message": "User not found!"}

        except Exception as e:
            file_logger.error(f"Database error getting user by username: {e}")
            stream_logger.error(
                f"Database error getting user by username: {e}"
            )
            raise e

    def get_user_by_email(self, email: str) -> Dict:
        """Get user data by email from database."""
        try:
            query = """
                SELECT id, username, email, hashed_password
                FROM users
                WHERE email = :email
            """
            result = self.query_db(query, {"email": email})

            if result:
                row = result.fetchone()
                if row:
                    return {
                        "id": row[0],
                        "username": row[1],
                        "email": row[2],
                        "hashed_password": row[3],
                        "message": "User found!",
                    }
            return {"message": "User not found!"}

        except Exception as e:
            file_logger.error(f"Database error getting user by email: {e}")
            stream_logger.error(f"Database error getting user by email: {e}")
            raise e

    def create_user(self, username: str, email: str, password: str) -> Dict:
        """Create a new user in the database."""
        # Check if user already exists
        if self.get_user_by_username(username).get("message") == "User found!":
            return {"message": "User already exists!"}

        try:
            # Hash the password
            hashed_password = bcrypt.hashpw(
                password.encode("utf-8"), bcrypt.gensalt()
            ).decode("utf-8")

            query = """
                INSERT INTO users (username, email, hashed_password)
                VALUES (:username, :email, :hashed_password)
                RETURNING id, username, email
            """

            result = self.query_db(
                query,
                {
                    "username": username,
                    "email": email,
                    "hashed_password": hashed_password,
                },
            )

            if result:
                row = result.fetchone()
                if row:
                    stream_logger.info(f"User created successfully!")
                    return {
                        "id": row[0],
                        "username": row[1],
                        "email": row[2],
                        "message": "User created successfully!",
                    }

            return {"message": "User already exists!"}

        except Exception as e:
            file_logger.error(f"Database error creating user: {e}")
            stream_logger.error(f"Database error creating user: {e}")
            raise e

    def create_cv_analysis_job(
        self,
        result: dict,
        username: str,
        cv_file_hash: str,
        company_name: str,
        job_title: str,
    ):
        """Create a new CV analysis job in the database."""
        try:
            query = """
                WITH user_id AS (
                SELECT
                    u.id
                FROM
                    users u
                WHERE
                    u.username = :username
                ),
                cv_id as (
                SELECT
                    cd.id
                FROM
                    cv_data cd
                WHERE
                    cd.file_hash = :cv_file_hash
                )
                INSERT INTO cv_analysis_jobs(
                    user_id,
                    cv_id,
                    company_name,
                    job_title,
                    raw_analysis_result
                )
                SELECT
                    user_id.id,
                    cv_id.id,
                    :company_name,
                    :job_title,
                    :result
                FROM user_id, cv_id
                RETURNING id;
            """

            job_result = self.query_db(
                query,
                {
                    "username": username,
                    "cv_file_hash": cv_file_hash,
                    "company_name": company_name,
                    "job_title": job_title,
                    "result": json.dumps(result),
                },
            )

            job_id = job_result.fetchone()[0] if job_result else None

            return {
                "message": "CV analysis job created successfully!",
                "job_id": job_id,
            }

        except Exception as e:
            file_logger.error(f"Database error creating CV analysis job: {e}")
            stream_logger.error(
                f"Database error creating CV analysis job: {e}"
            )
            raise e

    def get_cv_analysis_jobs(self, username):
        """Get all CV analysis jobs for a user from the database."""
        try:
            query = """
                SELECT
                    caj.*, u.username, cd.file_name
                FROM
                    cv_analysis_jobs caj
                    LEFT JOIN users u
                        ON caj.user_id = u.id
                    LEFT JOIN cv_data cd
                        ON caj.cv_id = cd.id
                WHERE u.username = :username
            """

            result = self.query_db(query, {"username": username})

            return (
                [
                    serialize_for_json(row._asdict())
                    for row in result.fetchall()
                ]
                if result
                else None
            )

        except Exception as e:

            file_logger.error(f"Database error getting CV analysis jobs: {e}")
            stream_logger.error(
                f"Database error getting CV analysis jobs: {e}"
            )

            raise e

    def get_cv_analysis_job_by_id(self, job_id):
        """Get a CV analysis job by id from the database."""
        try:
            query = """
                SELECT caj.*, u.username, cd.file_name
                FROM cv_analysis_jobs caj
                LEFT JOIN users u
                    ON caj.user_id = u.id
                LEFT JOIN cv_data cd
                    ON caj.cv_id = cd.id
                WHERE caj.id = :job_id
            """

            result = self.query_db(query, {"job_id": job_id})

            return serialize_for_json(result.fetchone()) if result else None

        except Exception as e:
            file_logger.error(
                f"Database error getting CV analysis job by id: {e}"
            )
            stream_logger.error(
                f"Database error getting CV analysis job by id: {e}"
            )
            raise e


class PGVectorClient:

    def __init__(self, embedding_function, collection_name, use_jsonb=True):
        self.connection_string = DATABASE_URL
        self.embedding_function = embedding_function
        self.collection_name = collection_name
        self.use_jsonb = use_jsonb
        self.pgvector_client = self._get_pgvector_client()

    def _get_pgvector_client(self):
        return PGVector(
            connection_string=self.connection_string,
            embedding_function=self.embedding_function,
            collection_name=self.collection_name,
            use_jsonb=self.use_jsonb,
        )

    def add_texts(self, texts, metadatas):
        try:
            self.pgvector_client.add_texts(texts, metadatas)
            stream_logger.info(f"Texts added to database successfully!")
        except Exception as e:
            file_logger.error(f"Failed to add texts: {e}")
            stream_logger.error(f"Failed to add texts: {e}")

    def similarity_search(self, query, metadata_filter, k=10):
        return self.pgvector_client.similarity_search(
            query, k, metadata_filter
        )


if __name__ == "__main__":
    postgres_client = PostgresClient()

    query = """
            SELECT DISTINCT jsonb_array_elements_text(lpe.cmetadata->'urls') as url
            FROM langchain_pg_embedding lpe
        """

    result = postgres_client.query_db(query)
    print(result)
