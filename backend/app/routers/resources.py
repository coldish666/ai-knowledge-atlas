from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy.orm import Session

from app.db.database import get_db
from app.schemas.resources import KnowledgeResourceRead, ResourceListResponse, ResourceUpdate
from app.services import resource_service

router = APIRouter(prefix="/api/resources", tags=["resources"])


@router.get("", response_model=ResourceListResponse)
def read_resources(
    type: str | None = Query(default=None),
    authority_level: str | None = None,
    difficulty: str | None = None,
    language: str | None = None,
    layer: int | None = None,
    q: str | None = None,
    db: Session = Depends(get_db),
):
    items = resource_service.list_resources(
        db,
        resource_type=type,
        authority_level=authority_level,
        difficulty=difficulty,
        language=language,
        layer=layer,
        q=q,
    )
    return {"items": items, "total": len(items)}


@router.get("/recommended", response_model=list[KnowledgeResourceRead])
def read_recommended_resources(slug: str, db: Session = Depends(get_db)):
    return resource_service.recommended_for_slug(db, slug)


@router.put("/{resource_id}", response_model=KnowledgeResourceRead)
def update_resource(resource_id: int, payload: ResourceUpdate, db: Session = Depends(get_db)):
    resource = resource_service.get_resource(db, resource_id)
    if not resource:
        raise HTTPException(status_code=404, detail="Resource not found")
    return resource_service.update_resource(db, resource, payload)


@router.delete("/{resource_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_resource(resource_id: int, db: Session = Depends(get_db)):
    resource = resource_service.get_resource(db, resource_id)
    if not resource:
        raise HTTPException(status_code=404, detail="Resource not found")
    resource_service.delete_resource(db, resource)
