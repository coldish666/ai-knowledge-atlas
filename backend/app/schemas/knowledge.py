from datetime import datetime
from typing import Literal

from pydantic import BaseModel, ConfigDict


class ORMModel(BaseModel):
    model_config = ConfigDict(from_attributes=True)


class KnowledgeNodeBase(ORMModel):
    id: int
    slug: str
    title: str
    layer: int
    category: str
    difficulty: str
    summary: str
    tags: list[str]
    prerequisites: list[str]
    next_topics: list[str]
    related_topics: list[str]


class KnowledgeNodeRead(KnowledgeNodeBase):
    definition: str
    intuition: str
    why_it_matters: str
    math_form: str
    formulas: list[str]
    code_example: str
    applications: list[str]
    misconceptions: list[str]
    prerequisites: list[str]
    next_topics: list[str]
    related_topics: list[str]
    recommended_resources: list[str]
    self_check_questions: list[str]
    extension_questions: list[str]
    created_at: datetime
    updated_at: datetime


class KnowledgeListResponse(BaseModel):
    items: list[KnowledgeNodeBase]
    total: int


class KnowledgeLayer(BaseModel):
    layer: int
    name: str
    count: int


class RelatedKnowledgeResponse(BaseModel):
    slug: str
    relation_type: Literal["prerequisite", "next", "related", "same_layer"]
    items: list[KnowledgeNodeBase]


class GraphNode(BaseModel):
    id: str
    title: str
    layer: int
    category: str
    difficulty: str
    tags: list[str]


class GraphEdge(BaseModel):
    source: str
    target: str
    relation_type: str


class GraphResponse(BaseModel):
    nodes: list[GraphNode]
    edges: list[GraphEdge]


class SearchResult(KnowledgeNodeBase):
    highlights: list[str] = []
