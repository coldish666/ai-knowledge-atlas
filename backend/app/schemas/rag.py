from datetime import datetime

from pydantic import BaseModel, ConfigDict


class ORMModel(BaseModel):
    model_config = ConfigDict(from_attributes=True)


class RagDocumentRead(ORMModel):
    id: int
    filename: str
    original_name: str
    content_type: str
    path: str
    uploaded_at: datetime


class RagUploadResponse(BaseModel):
    id: int
    original_name: str
    chunks: int


class RagAskRequest(BaseModel):
    question: str
    scope: str = "all"
    top_k: int = 5


class RagCitation(BaseModel):
    source_label: str
    content: str
    source_type: str
    document_id: int | None = None
    knowledge_slug: str | None = None


class RagAskResponse(BaseModel):
    answer: str
    citations: list[RagCitation]
