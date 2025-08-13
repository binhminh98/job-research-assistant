"""
Module to specify file upload services for job research assistant app.
"""

from api_utils.upload_api_utils import UploadApiUtils


class UploadServices:

    @staticmethod
    def upload_file_to_minio(file, file_content):
        return UploadApiUtils.upload_file_to_minio(file, file_content)
