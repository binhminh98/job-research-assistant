"""
Embeddings CRUD endpoints for the Job Research Assistant backend.
"""

from typing import Optional

from fastapi import APIRouter, status
from fastapi.responses import JSONResponse
from services.embeddings_data_crud_endpoints import EmbeddingsDataCrudServices

router = APIRouter(
    prefix="/embeddings_data",
    tags=["embeddings_data"],
)


@router.get("/get_company_names")
async def get_company_names(
    company_name: Optional[str] = None,
) -> JSONResponse:
    try:
        response = EmbeddingsDataCrudServices.get_company_names(company_name)

        if response:
            return JSONResponse(
                status_code=status.HTTP_200_OK, content=response
            )

        else:
            return JSONResponse(
                status_code=status.HTTP_408_REQUEST_TIMEOUT,
                content="Error getting company names!",
            )

    except Exception as e:
        return JSONResponse(
            status_code=status.HTTP_400_BAD_REQUEST, content=str(e)
        )


@router.get("/get_job_titles")
async def get_job_titles(
    company_name: Optional[str] = None,
) -> JSONResponse:
    try:
        response = EmbeddingsDataCrudServices.get_job_titles(company_name)

        if response:
            return JSONResponse(
                status_code=status.HTTP_200_OK, content=response
            )

        else:
            return JSONResponse(
                status_code=status.HTTP_408_REQUEST_TIMEOUT,
                content="Error getting job titles from company name!",
            )

    except Exception as e:
        return JSONResponse(
            status_code=status.HTTP_400_BAD_REQUEST, content=str(e)
        )
