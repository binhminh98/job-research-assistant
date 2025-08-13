"""
Module to specify file upload endpoints for job research assistant app.
"""

from fastapi import APIRouter, File, UploadFile, status
from fastapi.responses import JSONResponse
from pydantic_models.upload_models import FileUploadResponse
from services.upload_services import UploadServices

router = APIRouter(
    prefix="/upload_file",
    tags=["upload_file"],
)


@router.post("/")
async def upload_file(file: UploadFile = File(...)) -> JSONResponse:
    try:
        # Validate file extension
        FileUploadResponse(filename=str(file.filename))

        file_content = await file.read()

        response = UploadServices.upload_file_to_minio(file, file_content)

        if response:
            return JSONResponse(
                status_code=status.HTTP_200_OK, content=response
            )

        else:
            return JSONResponse(
                status_code=status.HTTP_408_REQUEST_TIMEOUT,
                content="MinIO Server error!",
            )

    except Exception as e:
        return JSONResponse(
            status_code=status.HTTP_400_BAD_REQUEST, content=str(e)
        )
