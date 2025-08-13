"""
Module to specify backend logic for the services for file upload to MinIO.
"""

import io
from pathlib import Path

from db_connectors.minio.minio_client import MinioClient
from general_utils.logging import get_logger
from minio.error import S3Error

file_logger = get_logger(
    "file_" + __name__,
    write_to_file=True,
    log_filepath=Path(r"logs/backend/file_upload_api_utils.log"),
)


stream_logger = get_logger(
    "stream_" + __name__,
)

minio_client = MinioClient()._init_client()

bucket_name = "jobsearch-original-files"


class UploadApiUtils:

    @staticmethod
    def upload_file_to_minio(file, file_content):
        if not minio_client.bucket_exists(bucket_name):
            minio_client.make_bucket(bucket_name)
            stream_logger.info(f"Bucket '{bucket_name}' created.")

        try:
            file_bytes = io.BytesIO(file_content)

            minio_client.put_object(
                bucket_name=bucket_name,
                object_name=file.filename,
                data=file_bytes,
                length=len(file_content),
                content_type=file.content_type,
            )

            stream_logger.info(f"File '{file.filename}' uploaded to MinIO.")

            return {"filename": file.filename, "message": "Upload successful!"}

        except S3Error as e:
            error_message = f"Error uploading file to MinIO: {str(e)}"

            file_logger.error(error_message)
            stream_logger.error(error_message)

            return error_message
