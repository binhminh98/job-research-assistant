"""
Embeddings data CRUD endpoints for the Job Research Assistant backend.
"""

from pathlib import Path

from db_connectors.postgres.postgres_client import PostgresClient
from general_utils.logging import get_logger
from general_utils.utils import get_matching_strings

POSTGRES_CLIENT = PostgresClient()

file_logger = get_logger(
    "file_" + __name__,
    write_to_file=True,
    log_filepath=Path(r"logs/backend/embeddings_data_crud_utils.log"),
)

stream_logger = get_logger(
    "stream_" + __name__,
)


class EmbeddingsDataCrudApiUtils:

    @staticmethod
    def get_company_names(company_name: str | None) -> dict | None:
        # Query to get all relevant company names from the database
        query = f"""
            SELECT DISTINCT lpe.cmetadata->>'company_name' AS company_name
            FROM langchain_pg_embedding lpe
            WHERE lpe.cmetadata->>'company_name' IS NOT NULL;
        """

        try:
            result = POSTGRES_CLIENT.query_db(query)

        except Exception as e:
            file_logger.error(f"Database error getting company names: {e}")
            stream_logger.error(f"Database error getting company names: {e}")
            return None

        known_company_names = (
            list({row[0] for row in result.fetchall()}) if result else list()
        )

        if company_name:
            company_names = get_matching_strings(
                company_name, known_company_names
            )

            return {
                "company_names": company_names,
                "message": (
                    "Company names found!"
                    if company_names
                    else "No company names found!"
                ),
            }
        else:
            return {
                "company_names": known_company_names,
                "message": (
                    "Relevant company names found!"
                    if known_company_names
                    else "No relevant company names found!"
                ),
            }

    @staticmethod
    def get_job_titles(
        company_name: str | None,
    ) -> dict | None:
        # Query to get all relevant job titles from the database
        query = f"""
            SELECT DISTINCT lpe.cmetadata->>'job_title' AS job_title
            FROM langchain_pg_embedding lpe
            WHERE
            	lpe.cmetadata->>'job_title' IS NOT null;
        """

        try:
            if company_name:
                query = (
                    query
                    + f" AND lpe.cmetadata->>'company_name' = :company_name"
                )

                result = POSTGRES_CLIENT.query_db(
                    query, {"company_name": company_name}
                )
            else:
                result = POSTGRES_CLIENT.query_db(query)

        except Exception as e:
            file_logger.error(f"Database error getting job titles: {e}")
            stream_logger.error(f"Database error getting job titles: {e}")
            return None

        job_titles = (
            list({row[0] for row in result.fetchall()}) if result else list()
        )

        return {
            "job_titles": job_titles,
            "message": (
                "Job titles found!" if job_titles else "No job titles found!"
            ),
        }
