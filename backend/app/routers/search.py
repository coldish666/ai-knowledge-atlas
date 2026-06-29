from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.db.database import get_db
from app.schemas.knowledge import SearchResult
from app.services.search_service import search

router = APIRouter(prefix="/api/search", tags=["search"])


@router.get("", response_model=list[SearchResult])
def search_knowledge(
    q: str | None = None,
    layer: int | None = None,
    tag: str | None = None,
    difficulty: str | None = None,
    db: Session = Depends(get_db),
):
    return search(db, q=q, layer=layer, tag=tag, difficulty=difficulty)
