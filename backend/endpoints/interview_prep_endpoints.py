"""
Module to specify interview endpoints for job research assistant app.
"""

from fastapi import APIRouter, status
from fastapi.responses import JSONResponse
from services.interview_prep_services import InterviewPrepServices

router = APIRouter(
    prefix="/interview_prep",
    tags=["interview_prep"],
)


@router.post("/")
async def generate_interview_preparation_materials(
    company_name: str,
    job_title: str,
) -> JSONResponse:
    try:
        response = (
            InterviewPrepServices.generate_interview_preparation_materials(
                company_name, job_title
            )
        )

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
