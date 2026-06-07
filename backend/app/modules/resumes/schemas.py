from datetime import datetime
from typing import Any

from pydantic import BaseModel, Field


class ResumeCreateRequest(BaseModel):
    title: str = Field(min_length=1, max_length=200)
    templateKey: str = Field(default="classic", min_length=1, max_length=80)


class ResumeUpdateRequest(BaseModel):
    title: str = Field(min_length=1, max_length=200)
    templateKey: str = Field(min_length=1, max_length=80)
    content: dict[str, Any] = Field(default_factory=dict)
    layout: dict[str, Any] = Field(default_factory=dict)


class ResumeResponse(BaseModel):
    id: str
    title: str
    templateKey: str
    content: dict[str, Any]
    layout: dict[str, Any]
    createdAt: datetime
    updatedAt: datetime


class ResumeListResponse(BaseModel):
    items: list[ResumeResponse]


class ResumeVersionResponse(BaseModel):
    id: str
    resumeId: str
    versionNumber: int
    title: str
    templateKey: str
    content: dict[str, Any]
    layout: dict[str, Any]
    createdAt: datetime
