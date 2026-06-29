from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.db.database import get_db
from app.schemas.knowledge import (
    KnowledgeLayer,
    KnowledgeListResponse,
    KnowledgeNodeBase,
    KnowledgeNodeRead,
    RelatedKnowledgeResponse,
)
from app.schemas.resources import KnowledgeResourceRead, ResourceCreate
from app.services.knowledge_service import get_by_slug, get_many_by_slugs, layers, list_knowledge, same_layer, tags
from app.services import resource_service

router = APIRouter(prefix="/api/knowledge", tags=["knowledge"])


@router.get("", response_model=KnowledgeListResponse)
def read_knowledge(
    layer: int | None = None,
    tag: str | None = None,
    difficulty: str | None = None,
    category: str | None = None,
    db: Session = Depends(get_db),
):
    items = list_knowledge(db, layer=layer, tag=tag, difficulty=difficulty, category=category)
    return {"items": items, "total": len(items)}


@router.get("/layers", response_model=list[KnowledgeLayer])
def read_layers(db: Session = Depends(get_db)):
    return layers(db)


@router.get("/tags", response_model=list[str])
def read_tags(db: Session = Depends(get_db)):
    return tags(db)


@router.get("/{slug}/resources", response_model=list[KnowledgeResourceRead])
def read_knowledge_resources(slug: str, db: Session = Depends(get_db)):
    node = get_by_slug(db, slug)
    if not node:
        raise HTTPException(status_code=404, detail="Knowledge node not found")
    return resource_service.resources_for_slug(db, slug)


@router.post("/{slug}/resources", response_model=KnowledgeResourceRead)
def create_knowledge_resource(slug: str, payload: ResourceCreate, db: Session = Depends(get_db)):
    node = get_by_slug(db, slug)
    if not node:
        raise HTTPException(status_code=404, detail="Knowledge node not found")
    return resource_service.create_resource(db, slug, payload)


@router.get("/{slug}", response_model=KnowledgeNodeRead)
def read_knowledge_detail(slug: str, db: Session = Depends(get_db)):
    node = get_by_slug(db, slug)
    if not node:
        raise HTTPException(status_code=404, detail="Knowledge node not found")
    return node


@router.get("/{slug}/related", response_model=RelatedKnowledgeResponse)
def read_related(slug: str, db: Session = Depends(get_db)):
    node = get_by_slug(db, slug)
    if not node:
        raise HTTPException(status_code=404, detail="Knowledge node not found")
    return {"slug": slug, "relation_type": "related", "items": get_many_by_slugs(db, node.related_topics)}


@router.get("/{slug}/prerequisites", response_model=RelatedKnowledgeResponse)
def read_prerequisites(slug: str, db: Session = Depends(get_db)):
    node = get_by_slug(db, slug)
    if not node:
        raise HTTPException(status_code=404, detail="Knowledge node not found")
    return {"slug": slug, "relation_type": "prerequisite", "items": get_many_by_slugs(db, node.prerequisites)}


@router.get("/{slug}/next", response_model=RelatedKnowledgeResponse)
def read_next(slug: str, db: Session = Depends(get_db)):
    node = get_by_slug(db, slug)
    if not node:
        raise HTTPException(status_code=404, detail="Knowledge node not found")
    return {"slug": slug, "relation_type": "next", "items": get_many_by_slugs(db, node.next_topics)}


@router.get("/{slug}/same-layer", response_model=list[KnowledgeNodeBase])
def read_same_layer(slug: str, db: Session = Depends(get_db)):
    node = get_by_slug(db, slug)
    if not node:
        raise HTTPException(status_code=404, detail="Knowledge node not found")
    return same_layer(db, node)
