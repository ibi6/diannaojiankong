from fastapi import APIRouter

from app.core.dependencies import CurrentUser, DbSession
from app.core.responses import success_response
from app.modules.auth.schemas import LoginRequest
from app.modules.auth.service import authenticate_user, to_user_response

router = APIRouter(prefix="/auth", tags=["auth"])


@router.post("/login")
def login(request: LoginRequest, db: DbSession):
    return success_response(authenticate_user(db, request.username, request.password).model_dump())


@router.get("/me")
def me(current_user: CurrentUser):
    return success_response(to_user_response(current_user).model_dump())


@router.post("/logout")
def logout():
    return success_response(None, "Logged out")
