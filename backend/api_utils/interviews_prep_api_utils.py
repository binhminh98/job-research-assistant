"""
Module to specify backend logic for the services for interviews preparation for job research assistant app.
"""

from pathlib import Path

from core_langchain.factory.chains_factory import ChainsFactory
from db_connectors.postgres.postgres_client import PostgresClient
from general_utils.logging import get_logger

file_logger = get_logger(
    "file_" + __name__,
    write_to_file=True,
    log_filepath=Path(r"logs/backend/interviews_prep_api_utils.log"),
)

stream_logger = get_logger(
    "stream_" + __name__,
)

POSTGRES_CLIENT = PostgresClient()


class InterviewsPrepApiUtils:
    @staticmethod
    def generate_interview_preparation_materials(company_name, job_title):

        complete_interview_preparation_chain = ChainsFactory(
            model_name="gpt-3.5-turbo", temperature=0.3
        ).create_complete_interview_preparation_chain()

        input_data = {
            "company_name": company_name,
            "job_title": job_title,
        }

        try:
            complete_interview_preparation_result = (
                complete_interview_preparation_chain.invoke(input_data)
            )
        except Exception as e:
            message = f"Error generating interview preparation materials: {e}"
            file_logger.error(message)
            stream_logger.error(message)
            return {
                "message": "Error generating interview preparation materials!"
            }

        return {
            "message": "Interview preparation materials generated successfully!",
            "result": complete_interview_preparation_result,
        }
