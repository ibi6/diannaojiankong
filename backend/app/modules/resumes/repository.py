from sqlalchemy import func, select
from sqlalchemy.orm import Session

from app.modules.resumes.models import Resume, ResumeVersion


def list_active_resumes(db: Session, user_id: int) -> list[Resume]:
    return list(
        db.scalars(
            select(Resume)
            .where(Resume.user_id == user_id, Resume.deleted.is_(False))
            .order_by(Resume.updated_at.desc())
        )
    )


def get_resume(db: Session, user_id: int, resume_id: str) -> Resume | None:
    return db.scalar(
        select(Resume).where(
            Resume.id == resume_id,
            Resume.user_id == user_id,
        )
    )


def next_version_number(db: Session, resume_id: str) -> int:
    current = db.scalar(
        select(func.max(ResumeVersion.version_number)).where(ResumeVersion.resume_id == resume_id)
    )
    return int(current or 0) + 1
