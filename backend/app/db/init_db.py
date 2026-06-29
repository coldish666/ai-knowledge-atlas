from sqlalchemy import select

from app.db.database import Base, SessionLocal, engine
from app.models.knowledge import KnowledgeNode, KnowledgeResource
from app.seed.seed_knowledge import seed_knowledge
from app.seed.seed_resources import seed_resources


def init_db() -> None:
    Base.metadata.create_all(bind=engine)
    with SessionLocal() as db:
        if db.scalar(select(KnowledgeNode).limit(1)) is None:
            seed_knowledge(db)
        if db.scalar(select(KnowledgeResource).limit(1)) is None:
            seed_resources(db)
