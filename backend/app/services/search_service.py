import re

from sqlalchemy import select
from sqlalchemy.orm import Session

from app.models import KnowledgeNode


SEARCH_FIELDS = [
    "title",
    "summary",
    "definition",
    "intuition",
    "why_it_matters",
    "math_form",
    "category",
    "difficulty",
]


def normalize(text: str) -> str:
    return text.lower().strip()


def node_text(node: KnowledgeNode) -> str:
    pieces = [str(getattr(node, field) or "") for field in SEARCH_FIELDS]
    pieces.extend(node.tags or [])
    pieces.extend(node.applications or [])
    pieces.extend(node.misconceptions or [])
    return "\n".join(pieces)


def highlights(node: KnowledgeNode, query: str) -> list[str]:
    if not query:
        return []
    q = normalize(query)
    results = []
    for part in [node.title, node.summary, node.definition, node.intuition, " ".join(node.tags or [])]:
        if q in normalize(part):
            results.append(re.sub(f"({re.escape(query)})", r"**\1**", part, flags=re.IGNORECASE)[:240])
    return results[:3]


def search(
    db: Session,
    q: str | None = None,
    layer: int | None = None,
    tag: str | None = None,
    difficulty: str | None = None,
) -> list[dict]:
    query = select(KnowledgeNode)
    if layer is not None:
        query = query.where(KnowledgeNode.layer == layer)
    if difficulty:
        query = query.where(KnowledgeNode.difficulty == difficulty)
    nodes = list(db.scalars(query.order_by(KnowledgeNode.layer, KnowledgeNode.id)).all())
    if tag:
        nodes = [node for node in nodes if tag in (node.tags or [])]
    if q:
        q_norm = normalize(q)
        nodes = [node for node in nodes if q_norm in normalize(node_text(node))]
    return [
        {
            "id": node.id,
            "slug": node.slug,
            "title": node.title,
            "layer": node.layer,
            "category": node.category,
            "difficulty": node.difficulty,
            "summary": node.summary,
            "tags": node.tags,
            "prerequisites": node.prerequisites or [],
            "next_topics": node.next_topics or [],
            "related_topics": node.related_topics or [],
            "highlights": highlights(node, q or ""),
        }
        for node in nodes
    ]
