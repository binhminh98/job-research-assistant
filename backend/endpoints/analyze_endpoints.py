"""
Module to specify analyze endpoints for job research assistant app.
"""

from typing import List, Optional

from fastapi import APIRouter, status
from fastapi.responses import JSONResponse
from services.analyze_services import AnalyzeServices

router = APIRouter(
    prefix="/analyze",
    tags=["analyze"],
)


@router.post("/extract_jd_urls")
async def extract_jd_urls(jd_urls: List[str]) -> JSONResponse:
    try:
        response = AnalyzeServices.extract_jd_urls(jd_urls, url_type="jd")

        if response:
            return JSONResponse(
                status_code=status.HTTP_200_OK, content=response
            )

        else:
            return JSONResponse(
                status_code=status.HTTP_408_REQUEST_TIMEOUT,
                content="There are no new URLs to extract!",
            )

    except Exception as e:
        return JSONResponse(
            status_code=status.HTTP_400_BAD_REQUEST, content=str(e)
        )


@router.post("/extract_company_urls")
async def extract_company_urls(company_urls: List[str]) -> JSONResponse:
    try:
        response = AnalyzeServices.extract_company_urls(
            company_urls, url_type="company"
        )

        if response:
            return JSONResponse(
                status_code=status.HTTP_200_OK, content=response
            )

        else:
            return JSONResponse(
                status_code=status.HTTP_408_REQUEST_TIMEOUT,
                content="There are no new URLs to extract!",
            )

    except Exception as e:
        return JSONResponse(
            status_code=status.HTTP_400_BAD_REQUEST, content=str(e)
        )


@router.post("/analyze_cv")
async def analyze(
    username: str,
    cv_object_key: str,
    company_name: str,
    job_title: str,
) -> JSONResponse:
    try:
        response = AnalyzeServices.analyze(
            username, cv_object_key, company_name, job_title
        )

        if response:
            return JSONResponse(
                status_code=status.HTTP_200_OK, content=response
            )

        else:
            return JSONResponse(
                status_code=status.HTTP_408_REQUEST_TIMEOUT,
                content="Error analyzing CV!",
            )

    except Exception as e:
        return JSONResponse(
            status_code=status.HTTP_400_BAD_REQUEST, content=str(e)
        )


@router.get("/get_cv_analysis_jobs")
async def get_cv_analysis_jobs(username: str) -> JSONResponse:
    try:
        response = AnalyzeServices.get_cv_analysis_jobs(username)

        if response:
            return JSONResponse(
                status_code=status.HTTP_200_OK, content=response
            )

        else:
            return JSONResponse(
                status_code=status.HTTP_408_REQUEST_TIMEOUT,
                content="There are no analysis jobs!",
            )

    except Exception as e:
        return JSONResponse(
            status_code=status.HTTP_400_BAD_REQUEST, content=str(e)
        )


@router.get("/get_cv_analysis_job_by_id")
async def get_cv_analysis_job_by_id(job_id: int) -> JSONResponse:
    try:
        response = AnalyzeServices.get_cv_analysis_job_by_id(job_id)

        if response:
            return JSONResponse(
                status_code=status.HTTP_200_OK, content=response
            )

        else:
            return JSONResponse(
                status_code=status.HTTP_408_REQUEST_TIMEOUT,
                content="Job not found!",
            )

    except Exception as e:
        return JSONResponse(
            status_code=status.HTTP_400_BAD_REQUEST, content=str(e)
        )
