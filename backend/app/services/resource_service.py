from sqlalchemy import select
from sqlalchemy.orm import Session

from app.models import KnowledgeNode, KnowledgeResource
from app.schemas.resources import ResourceCreate, ResourceUpdate


TYPE_PRIORITY = {
    "official_doc": 0,
    "course": 1,
    "paper": 2,
    "book": 3,
    "video": 4,
    "code": 5,
    "chinese_note": 6,
    "blog": 7,
}

AUTHORITY_PRIORITY = {"S": 0, "A": 1, "B": 2, "C": 3}
DIFFICULTY_PRIORITY = {"beginner": 0, "intermediate": 1, "advanced": 2}


def sort_resources(resources: list[KnowledgeResource]) -> list[KnowledgeResource]:
    return sorted(
        resources,
        key=lambda item: (
            AUTHORITY_PRIORITY.get(item.authority_level, 9),
            TYPE_PRIORITY.get(item.resource_type, 9),
            DIFFICULTY_PRIORITY.get(item.difficulty, 9),
            item.source,
            item.title,
        ),
    )


def list_resources(
    db: Session,
    resource_type: str | None = None,
    authority_level: str | None = None,
    difficulty: str | None = None,
    language: str | None = None,
    layer: int | None = None,
    q: str | None = None,
) -> list[KnowledgeResource]:
    query = select(KnowledgeResource)
    if layer is not None:
        query = query.join(KnowledgeNode, KnowledgeNode.slug == KnowledgeResource.knowledge_slug).where(KnowledgeNode.layer == layer)
    if resource_type:
        query = query.where(KnowledgeResource.resource_type == resource_type)
    if authority_level:
        query = query.where(KnowledgeResource.authority_level == authority_level)
    if difficulty:
        query = query.where(KnowledgeResource.difficulty == difficulty)
    if language:
        query = query.where(KnowledgeResource.language == language)
    resources = list(db.scalars(query.order_by(KnowledgeResource.knowledge_slug, KnowledgeResource.id)).all())
    if q:
        needle = q.lower().strip()
        resources = [
            item for item in resources
            if needle in f"{item.title} {item.description} {item.why_recommended} {item.source} {' '.join(item.tags or [])}".lower()
        ]
    return sort_resources(resources)


def resources_for_slug(db: Session, slug: str) -> list[KnowledgeResource]:
    return sort_resources(list(db.scalars(select(KnowledgeResource).where(KnowledgeResource.knowledge_slug == slug)).all()))


def recommended_for_slug(db: Session, slug: str, limit: int = 6) -> list[KnowledgeResource]:
    return resources_for_slug(db, slug)[:limit]


def get_resource(db: Session, resource_id: int) -> KnowledgeResource | None:
    return db.get(KnowledgeResource, resource_id)


def create_resource(db: Session, slug: str, data: ResourceCreate) -> KnowledgeResource:
    resource = KnowledgeResource(knowledge_slug=slug, **data.model_dump(mode="json"))
    db.add(resource)
    db.commit()
    db.refresh(resource)
    return resource


def update_resource(db: Session, resource: KnowledgeResource, data: ResourceUpdate) -> KnowledgeResource:
    for key, value in data.model_dump(exclude_unset=True, mode="json").items():
        setattr(resource, key, value)
    db.commit()
    db.refresh(resource)
    return resource


def delete_resource(db: Session, resource: KnowledgeResource) -> None:
    db.delete(resource)
    db.commit()
