"""
    Module to specify Pydantic models for the upload endpoints.
"""

from pydantic import BaseModel, field_validator

ALLOWED_FILE_EXTENSIONS = {".pdf", ".docx", ".doc"}


class FileUploadResponse(BaseModel):
    filename: str

    @field_validator("filename")
    def validate_file_extension(cls, v):
        if not any(v.lower().endswith(ext) for ext in ALLOWED_FILE_EXTENSIONS):
            raise ValueError(
                f"File type not supported!. Supported file types are: {ALLOWED_FILE_EXTENSIONS}"
            )
        return v
