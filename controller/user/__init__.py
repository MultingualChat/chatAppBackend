from validators.error import FieldError
from fastapi import APIRouter
from .crud import create_new_user, edit_user
from.schemas import UserCreateResponse, UserEdit, UserObjResponse


router = APIRouter(
    tags=["user"],
    dependencies=[],
    responses={404: {"description": "Not found"}},
)


router.add_api_route(
    "/create",
    create_new_user,
    responses={
        200: {"model": UserCreateResponse},
        400: {"model": FieldError}
    },
    methods=["POST"]
)

router.add_api_route(
    "/update",
    edit_user,
    responses={
        200: {"model": UserObjResponse},
        400: {"model": FieldError}
    },
    methods=["PATCH"]
)

