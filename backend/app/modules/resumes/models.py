from sqlalchemy import Boolean, DateTime, ForeignKey, Integer, JSON, String
from sqlalchemy.orm import Mapped, mapped_column

from app.core.database import Base
from app.shared.ids import new_id
from app.shared.time import utc_now


class Resume(Base):
    __tablename__ = "resumes"

    id: Mapped[str] = mapped_column(String(64), primary_key=True, default=new_id)
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id"), nullable=False, index=True)
    title: Mapped[str] = mapped_column(String(200), nullable=False)
    template_key: Mapped[str] = mapped_column(String(80), nullable=False, default="classic")
    content_json: Mapped[dict] = mapped_column(JSON, nullable=False, default=dict)
    layout_json: Mapped[dict] = mapped_column(JSON, nullable=False, default=dict)
    snapshot_hash: Mapped[str | None] = mapped_column(String(128), nullable=True)
    deleted: Mapped[bool] = mapped_column(Boolean, nullable=False, default=False, index=True)
    created_at: Mapped[DateTime] = mapped_column(DateTime, nullable=False, default=utc_now)
    updated_at: Mapped[DateTime] = mapped_column(DateTime, nullable=False, default=utc_now, onupdate=utc_now)
    deleted_at: Mapped[DateTime | None] = mapped_column(DateTime, nullable=True)


class ResumeVersion(Base):
    __tablename__ = "resume_versions"

    id: Mapped[str] = mapped_column(String(64), primary_key=True, default=new_id)
    resume_id: Mapped[str] = mapped_column(ForeignKey("resumes.id"), nullable=False, index=True)
    version_number: Mapped[int] = mapped_column(Integer, nullable=False)
    title: Mapped[str] = mapped_column(String(200), nullable=False)
    template_key: Mapped[str] = mapped_column(String(80), nullable=False)
    content_json: Mapped[dict] = mapped_column(JSON, nullable=False, default=dict)
    layout_json: Mapped[dict] = mapped_column(JSON, nullable=False, default=dict)
    created_at: Mapped[DateTime] = mapped_column(DateTime, nullable=False, default=utc_now)
