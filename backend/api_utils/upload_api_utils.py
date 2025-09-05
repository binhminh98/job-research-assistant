"""
Module to specify backend logic for the services for file upload to MinIO.
"""

import hashlib
import io
from pathlib import Path

from core_langchain.base_chains.cv_chains import CVParserChain
from db_connectors.minio.minio_client import MinioClient
from db_connectors.postgres.postgres_client import PostgresClient
from general_utils.logging import get_logger
from minio.error import S3Error
from pydantic_models.postgres_be_models import CVData, User

file_logger = get_logger(
    "file_" + __name__,
    write_to_file=True,
    log_filepath=Path(r"logs/backend/file_upload_api_utils.log"),
)


stream_logger = get_logger(
    "stream_" + __name__,
)

MINIO_CLIENT = MinioClient()
POSTGRES_CLIENT = PostgresClient()
BUCKET_NAME = "jobsearch-original-files"


class UploadApiUtils:

    @staticmethod
    def upload_file(file, file_content, username):
        # Check if file already exists in MinIO and upload if not
        file_bytes = io.BytesIO(file_content)
        file_hash = hashlib.sha256(file_content).hexdigest()
        object_key = f"{file_hash}/{file.filename}"

        try:
            MINIO_CLIENT.minio_client.stat_object(BUCKET_NAME, object_key)

            return {
                "object_key": object_key,
                "message": "File already exists!",
            }

        except S3Error as e:
            if e.code == "NoSuchKey":
                pass
            else:
                error_message = f"Error uploading file to MinIO: {str(e)}"

                file_logger.error(error_message)
                stream_logger.error(error_message)

        if not MINIO_CLIENT.minio_client.bucket_exists(BUCKET_NAME):
            MINIO_CLIENT.minio_client.make_bucket(BUCKET_NAME)
            stream_logger.info(f"Bucket '{BUCKET_NAME}' created.")

        try:
            MINIO_CLIENT.minio_client.put_object(
                bucket_name=BUCKET_NAME,
                object_name=object_key,
                data=file_bytes,
                length=len(file_content),
                content_type=file.content_type,
            )

            stream_logger.info(f"File '{file.filename}' uploaded to MinIO.")

        except S3Error as e:
            error_message = f"Error uploading file to MinIO: {str(e)}"

            file_logger.error(error_message)
            stream_logger.error(error_message)

        # Run CV extraction chain and ingest into database
        raw_object = MINIO_CLIENT.get_object_using_langchain_s3_loader(
            BUCKET_NAME, object_key
        )

        raw_text = raw_object[0].page_content
        cv_file_path = raw_object[0].metadata["source"]
        cv_file_name = cv_file_path.split("/")[-1]
        cv_file_hash = cv_file_path.split("/")[-2]

        cv_parser_chain = CVParserChain(
            model_name="gpt-3.5-turbo", temperature=0.3
        )

        cv_parser_result = cv_parser_chain.run_chain({"raw_cv_text": raw_text})

        # Create a new session using context management
        with PostgresClient()._get_connection_context() as session:
            # Assuming you have already created a user
            user = session.query(User).filter_by(username=username).first()

            # Create a new CVData instance
            new_cv = CVData(
                user_id=user.id,
                file_path=cv_file_path,
                file_name=cv_file_name,
                file_hash=cv_file_hash,
                raw_text=raw_text,
                extracted_text=cv_parser_result,
                contact=cv_parser_result["contact"],
                certifications=cv_parser_result["certifications"],
                skills=cv_parser_result["skills"],
                summary=cv_parser_result["summary"],
                languages=cv_parser_result["languages"],
                education=cv_parser_result["education"],
                experience=cv_parser_result["experience"],
            )

            # Add the new CV to the session
            session.add(new_cv)

            # Commit the session
            session.commit()

        return {
            "object_key": object_key,
            "message": "Upload CV to MinIO and ingest metadata to database successfully!",
        }
