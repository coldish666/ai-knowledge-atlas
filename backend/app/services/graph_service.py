from sqlalchemy import select
from sqlalchemy.orm import Session

from app.models import KnowledgeNode, KnowledgeRelation


def graph(db: Session, layer: int | None = None) -> dict:
    node_query = select(KnowledgeNode)
    if layer is not None:
        node_query = node_query.where(KnowledgeNode.layer == layer)
    nodes = list(db.scalars(node_query.order_by(KnowledgeNode.layer, KnowledgeNode.id)).all())
    node_slugs = {node.slug for node in nodes}
    edges = [
        relation
        for relation in db.scalars(select(KnowledgeRelation)).all()
        if relation.source_slug in node_slugs and relation.target_slug in node_slugs
    ]
    return {
        "nodes": [
            {
                "id": node.slug,
                "title": node.title,
                "layer": node.layer,
                "category": node.category,
                "difficulty": node.difficulty,
                "tags": node.tags,
            }
            for node in nodes
        ],
        "edges": [
            {
                "source": edge.source_slug,
                "target": edge.target_slug,
                "relation_type": edge.relation_type,
            }
            for edge in edges
        ],
    }


def neighborhood(db: Session, slug: str) -> dict:
    relations = list(
        db.scalars(
            select(KnowledgeRelation).where(
                (KnowledgeRelation.source_slug == slug) | (KnowledgeRelation.target_slug == slug)
            )
        ).all()
    )
    slugs = {slug}
    for relation in relations:
        slugs.add(relation.source_slug)
        slugs.add(relation.target_slug)
    nodes = list(db.scalars(select(KnowledgeNode).where(KnowledgeNode.slug.in_(slugs))).all())
    return {
        "nodes": [
            {
                "id": node.slug,
                "title": node.title,
                "layer": node.layer,
                "category": node.category,
                "difficulty": node.difficulty,
                "tags": node.tags,
            }
            for node in nodes
        ],
        "edges": [
            {
                "source": relation.source_slug,
                "target": relation.target_slug,
                "relation_type": relation.relation_type,
            }
            for relation in relations
        ],
    }
