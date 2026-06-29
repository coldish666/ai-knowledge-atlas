from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.db.database import get_db
from app.schemas.knowledge import GraphResponse
from app.services.graph_service import graph, neighborhood

router = APIRouter(prefix="/api/graph", tags=["graph"])


@router.get("", response_model=GraphResponse)
def read_graph(layer: int | None = None, db: Session = Depends(get_db)):
    return graph(db, layer=layer)


@router.get("/{slug}/neighborhood", response_model=GraphResponse)
def read_neighborhood(slug: str, db: Session = Depends(get_db)):
    return neighborhood(db, slug)
