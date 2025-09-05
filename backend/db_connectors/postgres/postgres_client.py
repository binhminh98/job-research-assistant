"""
Helper module to connect to Postgres and perform operations like querying the database.
"""

from pathlib import Path
from typing import Any

from config import (
    POSTGRES_DB,
    POSTGRES_HOST,
    POSTGRES_PASSWORD,
    POSTGRES_PORT,
    POSTGRES_USER,
)
from general_utils.logging import get_logger
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
                stream_logger.info(f"Query executed successfully!")
                return result

        except Exception as e:
            file_logger.error(f"Failed to query database: {e}")
            stream_logger.error(f"Failed to query database: {e}")
            return None


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
