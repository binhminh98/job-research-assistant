"""
Module to specify file upload services for job research assistant app.
"""

from api_utils.upload_api_utils import UploadApiUtils


class UploadServices:

    @staticmethod
    def upload_file(file, file_content, username):
        return UploadApiUtils.upload_file(file, file_content, username)
