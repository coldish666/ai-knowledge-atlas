from datetime import datetime

from pydantic import BaseModel, ConfigDict, HttpUrl


class ResourceBase(BaseModel):
    title: str
    url: HttpUrl
    source: str
    resource_type: str
    authority_level: str
    difficulty: str
    language: str
    estimated_time: str = ""
    description: str
    why_recommended: str
    tags: list[str] = []


class ResourceCreate(ResourceBase):
    pass


class ResourceUpdate(BaseModel):
    title: str | None = None
    url: HttpUrl | None = None
    source: str | None = None
    resource_type: str | None = None
    authority_level: str | None = None
    difficulty: str | None = None
    language: str | None = None
    estimated_time: str | None = None
    description: str | None = None
    why_recommended: str | None = None
    tags: list[str] | None = None


class KnowledgeResourceRead(ResourceBase):
    model_config = ConfigDict(from_attributes=True)

    id: int
    knowledge_slug: str
    created_at: datetime
    updated_at: datetime


class ResourceListResponse(BaseModel):
    items: list[KnowledgeResourceRead]
    total: int
