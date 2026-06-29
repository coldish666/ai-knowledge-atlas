from sqlalchemy import select
from sqlalchemy.orm import Session

from app.models import KnowledgeNode
from app.seed.seed_knowledge import LAYER_NAMES


def list_knowledge(
    db: Session,
    layer: int | None = None,
    tag: str | None = None,
    difficulty: str | None = None,
    category: str | None = None,
) -> list[KnowledgeNode]:
    query = select(KnowledgeNode)
    if layer is not None:
        query = query.where(KnowledgeNode.layer == layer)
    if difficulty:
        query = query.where(KnowledgeNode.difficulty == difficulty)
    if category:
        query = query.where(KnowledgeNode.category == category)
    nodes = list(db.scalars(query.order_by(KnowledgeNode.layer, KnowledgeNode.category, KnowledgeNode.id)).all())
    if tag:
        nodes = [node for node in nodes if tag in (node.tags or [])]
    return nodes


def get_by_slug(db: Session, slug: str) -> KnowledgeNode | None:
    return db.scalar(select(KnowledgeNode).where(KnowledgeNode.slug == slug))


def get_many_by_slugs(db: Session, slugs: list[str]) -> list[KnowledgeNode]:
    if not slugs:
        return []
    nodes = list(db.scalars(select(KnowledgeNode).where(KnowledgeNode.slug.in_(slugs))).all())
    order = {slug: index for index, slug in enumerate(slugs)}
    return sorted(nodes, key=lambda node: order.get(node.slug, 9999))


def layers(db: Session) -> list[dict]:
    nodes = list(db.scalars(select(KnowledgeNode)).all())
    return [
        {
            "layer": layer,
            "name": name,
            "count": sum(1 for node in nodes if node.layer == layer),
        }
        for layer, name in LAYER_NAMES.items()
    ]


def tags(db: Session) -> list[str]:
    values: set[str] = set()
    for node in db.scalars(select(KnowledgeNode)).all():
        values.update(node.tags or [])
    return sorted(values)


def same_layer(db: Session, node: KnowledgeNode, limit: int = 8) -> list[KnowledgeNode]:
    return list(
        db.scalars(
            select(KnowledgeNode)
            .where(KnowledgeNode.layer == node.layer, KnowledgeNode.slug != node.slug)
            .order_by(KnowledgeNode.category, KnowledgeNode.title)
            .limit(limit)
        ).all()
    )
