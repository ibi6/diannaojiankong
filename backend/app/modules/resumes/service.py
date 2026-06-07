from sqlalchemy.orm import Session

from app.core.exceptions import NotFoundError
from app.modules.resumes.models import Resume, ResumeVersion
from app.modules.resumes.repository import get_resume, list_active_resumes, next_version_number
from app.modules.resumes.schemas import (
    ResumeCreateRequest,
    ResumeListResponse,
    ResumeResponse,
    ResumeUpdateRequest,
    ResumeVersionResponse,
)
from app.shared.time import utc_now


def to_resume_response(resume: Resume) -> ResumeResponse:
    return ResumeResponse(
        id=resume.id,
        title=resume.title,
        templateKey=resume.template_key,
        content=resume.content_json,
        layout=resume.layout_json,
        createdAt=resume.created_at,
        updatedAt=resume.updated_at,
    )


def to_version_response(version: ResumeVersion) -> ResumeVersionResponse:
    return ResumeVersionResponse(
        id=version.id,
        resumeId=version.resume_id,
        versionNumber=version.version_number,
        title=version.title,
        templateKey=version.template_key,
        content=version.content_json,
        layout=version.layout_json,
        createdAt=version.created_at,
    )


def list_resumes(db: Session, user_id: int) -> ResumeListResponse:
    return ResumeListResponse(items=[to_resume_response(item) for item in list_active_resumes(db, user_id)])


def create_resume(db: Session, user_id: int, request: ResumeCreateRequest) -> ResumeResponse:
    resume = Resume(
        user_id=user_id,
        title=request.title,
        template_key=request.templateKey,
        content_json={"basics": {}, "sections": []},
        layout_json={"sections": ["basics"]},
    )
    db.add(resume)
    db.commit()
    db.refresh(resume)
    return to_resume_response(resume)


def require_resume(db: Session, user_id: int, resume_id: str) -> Resume:
    resume = get_resume(db, user_id, resume_id)
    if resume is None:
        raise NotFoundError("Resume not found")
    return resume


def update_resume(
    db: Session,
    user_id: int,
    resume_id: str,
    request: ResumeUpdateRequest,
) -> ResumeResponse:
    resume = require_resume(db, user_id, resume_id)
    resume.title = request.title
    resume.template_key = request.templateKey
    resume.content_json = request.content
    resume.layout_json = request.layout
    resume.updated_at = utc_now()
    db.commit()
    db.refresh(resume)
    return to_resume_response(resume)


def soft_delete_resume(db: Session, user_id: int, resume_id: str) -> None:
    resume = require_resume(db, user_id, resume_id)
    resume.deleted = True
    resume.deleted_at = utc_now()
    resume.updated_at = utc_now()
    db.commit()


def create_version(db: Session, user_id: int, resume_id: str) -> ResumeVersionResponse:
    resume = require_resume(db, user_id, resume_id)
    version = ResumeVersion(
        resume_id=resume.id,
        version_number=next_version_number(db, resume.id),
        title=resume.title,
        template_key=resume.template_key,
        content_json=resume.content_json,
        layout_json=resume.layout_json,
    )
    db.add(version)
    db.commit()
    db.refresh(version)
    return to_version_response(version)
