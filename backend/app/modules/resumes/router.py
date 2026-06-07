from fastapi import APIRouter

from app.core.dependencies import CurrentUser, DbSession
from app.core.responses import success_response
from app.modules.resumes.schemas import ResumeCreateRequest, ResumeUpdateRequest
from app.modules.resumes.service import (
    create_resume,
    create_version,
    list_resumes,
    soft_delete_resume,
    to_resume_response,
    update_resume,
    require_resume,
)

router = APIRouter(prefix="/resumes", tags=["resumes"])


@router.get("")
def list_resume_endpoint(db: DbSession, current_user: CurrentUser):
    return success_response(list_resumes(db, current_user.id).model_dump())


@router.post("")
def create_resume_endpoint(request: ResumeCreateRequest, db: DbSession, current_user: CurrentUser):
    return success_response(create_resume(db, current_user.id, request).model_dump())


@router.get("/{resume_id}")
def get_resume_endpoint(resume_id: str, db: DbSession, current_user: CurrentUser):
    return success_response(to_resume_response(require_resume(db, current_user.id, resume_id)).model_dump())


@router.put("/{resume_id}")
def update_resume_endpoint(
    resume_id: str,
    request: ResumeUpdateRequest,
    db: DbSession,
    current_user: CurrentUser,
):
    return success_response(update_resume(db, current_user.id, resume_id, request).model_dump())


@router.delete("/{resume_id}")
def delete_resume_endpoint(resume_id: str, db: DbSession, current_user: CurrentUser):
    soft_delete_resume(db, current_user.id, resume_id)
    return success_response(None, "Resume deleted")


@router.post("/{resume_id}/versions")
def create_version_endpoint(resume_id: str, db: DbSession, current_user: CurrentUser):
    return success_response(create_version(db, current_user.id, resume_id).model_dump())
