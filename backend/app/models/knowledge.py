from datetime import datetime

from sqlalchemy import DateTime, ForeignKey, Integer, JSON, String, Text, UniqueConstraint
from sqlalchemy.orm import Mapped, mapped_column

from app.db.database import Base


class KnowledgeNode(Base):
    __tablename__ = "knowledge_nodes"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    slug: Mapped[str] = mapped_column(String(140), unique=True, index=True)
    title: Mapped[str] = mapped_column(String(180), index=True)
    layer: Mapped[int] = mapped_column(Integer, index=True)
    category: Mapped[str] = mapped_column(String(120), index=True)
    difficulty: Mapped[str] = mapped_column(String(40), index=True)
    summary: Mapped[str] = mapped_column(Text)
    definition: Mapped[str] = mapped_column(Text)
    intuition: Mapped[str] = mapped_column(Text)
    why_it_matters: Mapped[str] = mapped_column(Text)
    math_form: Mapped[str] = mapped_column(Text)
    formulas: Mapped[list[str]] = mapped_column(JSON, default=list)
    code_example: Mapped[str] = mapped_column(Text)
    applications: Mapped[list[str]] = mapped_column(JSON, default=list)
    misconceptions: Mapped[list[str]] = mapped_column(JSON, default=list)
    prerequisites: Mapped[list[str]] = mapped_column(JSON, default=list)
    next_topics: Mapped[list[str]] = mapped_column(JSON, default=list)
    related_topics: Mapped[list[str]] = mapped_column(JSON, default=list)
    tags: Mapped[list[str]] = mapped_column(JSON, default=list)
    recommended_resources: Mapped[list[str]] = mapped_column(JSON, default=list)
    self_check_questions: Mapped[list[str]] = mapped_column(JSON, default=list)
    extension_questions: Mapped[list[str]] = mapped_column(JSON, default=list)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)
    updated_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)


class KnowledgeRelation(Base):
    __tablename__ = "knowledge_relations"
    __table_args__ = (UniqueConstraint("source_slug", "target_slug", "relation_type"),)

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    source_slug: Mapped[str] = mapped_column(String(140), ForeignKey("knowledge_nodes.slug"), index=True)
    target_slug: Mapped[str] = mapped_column(String(140), ForeignKey("knowledge_nodes.slug"), index=True)
    relation_type: Mapped[str] = mapped_column(String(40), index=True)


class KnowledgeResource(Base):
    __tablename__ = "knowledge_resources"
    __table_args__ = (UniqueConstraint("knowledge_slug", "url"),)

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    knowledge_slug: Mapped[str] = mapped_column(String(140), ForeignKey("knowledge_nodes.slug"), index=True)
    title: Mapped[str] = mapped_column(String(260), index=True)
    url: Mapped[str] = mapped_column(Text)
    source: Mapped[str] = mapped_column(String(120), index=True)
    resource_type: Mapped[str] = mapped_column(String(40), index=True)
    authority_level: Mapped[str] = mapped_column(String(1), index=True)
    difficulty: Mapped[str] = mapped_column(String(40), index=True)
    language: Mapped[str] = mapped_column(String(16), index=True)
    estimated_time: Mapped[str] = mapped_column(String(40), default="")
    description: Mapped[str] = mapped_column(Text)
    why_recommended: Mapped[str] = mapped_column(Text)
    tags: Mapped[list[str]] = mapped_column(JSON, default=list)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)
    updated_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
