"""
Users CRUD endpoints for the Job Research Assistant backend.
"""

from fastapi import APIRouter, status
from fastapi.responses import JSONResponse
from pydantic_models.users_crud_models import UserCreateRequest
from services.users_crud_services import UsersServices

router = APIRouter(
    prefix="/users",
    tags=["users"],
)


@router.get("/")
async def get_users() -> JSONResponse:
    try:
        response = UsersServices.get_users()

        if response:
            return JSONResponse(
                status_code=status.HTTP_200_OK, content=response
            )

        else:
            return JSONResponse(
                status_code=status.HTTP_408_REQUEST_TIMEOUT,
                content="Database Server error!",
            )

    except Exception as e:
        return JSONResponse(
            status_code=status.HTTP_400_BAD_REQUEST, content=str(e)
        )


@router.post("/create_user")
async def create_user(user: UserCreateRequest) -> JSONResponse:
    try:
        response = UsersServices.create_user(user.model_dump())

        if response:
            return JSONResponse(
                status_code=status.HTTP_200_OK, content=response
            )

        else:
            return JSONResponse(
                status_code=status.HTTP_408_REQUEST_TIMEOUT,
                content="Database Server error!",
            )

    except Exception as e:
        return JSONResponse(
            status_code=status.HTTP_400_BAD_REQUEST, content=str(e)
        )


@router.get("/get_user/{username}")
async def get_user_by_username(username: str) -> JSONResponse:
    try:
        response = UsersServices.get_user_by_username(username)

        if response:
            return JSONResponse(
                status_code=status.HTTP_200_OK, content=response
            )

        else:
            return JSONResponse(
                status_code=status.HTTP_408_REQUEST_TIMEOUT,
                content="User not found!",
            )

    except Exception as e:
        return JSONResponse(
            status_code=status.HTTP_400_BAD_REQUEST, content=str(e)
        )


@router.get("/get_user/{email}")
async def get_user_by_email(email: str) -> JSONResponse:
    try:
        response = UsersServices.get_user_by_email(email)

        if response:
            return JSONResponse(
                status_code=status.HTTP_200_OK, content=response
            )

        else:
            return JSONResponse(
                status_code=status.HTTP_408_REQUEST_TIMEOUT,
                content="User not found by email!",
            )

    except Exception as e:
        return JSONResponse(
            status_code=status.HTTP_400_BAD_REQUEST, content=str(e)
        )
