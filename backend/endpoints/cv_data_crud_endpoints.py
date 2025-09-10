"""
CV data CRUD endpoints for the Job Research Assistant backend.
"""

from fastapi import APIRouter, status
from fastapi.responses import JSONResponse
from services.cv_data_crud_services import CVDataCrudServices

router = APIRouter(
    prefix="/cv_data",
    tags=["cv_data"],
)


@router.get("/get_cv_data_by_username/{username}")
async def get_cv_data_by_username(username: str) -> JSONResponse:
    try:
        response = CVDataCrudServices.get_cv_data_by_username(username)

        if response:
            return JSONResponse(
                status_code=status.HTTP_200_OK, content=response
            )

        else:
            return JSONResponse(
                status_code=status.HTTP_408_REQUEST_TIMEOUT,
                content="CV data not found!",
            )

    except Exception as e:
        return JSONResponse(
            status_code=status.HTTP_400_BAD_REQUEST, content=str(e)
        )


@router.get("/get_cv_data_by_file_hash/{file_hash}")
async def get_cv_data_by_file_hash(file_hash: str) -> JSONResponse:
    try:
        response = CVDataCrudServices.get_cv_data_by_file_hash(file_hash)

        if response:
            return JSONResponse(
                status_code=status.HTTP_200_OK, content=response
            )

        else:
            return JSONResponse(
                status_code=status.HTTP_408_REQUEST_TIMEOUT,
                content="CV data not found!",
            )

    except Exception as e:
        return JSONResponse(
            status_code=status.HTTP_400_BAD_REQUEST, content=str(e)
        )
