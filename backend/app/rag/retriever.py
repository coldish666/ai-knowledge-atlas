from sqlalchemy import select
from sqlalchemy.orm import Session

from app.models import KnowledgeNode, RagChunk
from app.rag.chunker import keywords


def score_text(query_terms: set[str], text: str, token_list: list[str] | None = None) -> int:
    lowered = text.lower()
    token_hits = len(query_terms & set(token_list or []))
    exact_hits = sum(1 for term in query_terms if term in lowered)
    return token_hits * 2 + exact_hits


def retrieve(db: Session, question: str, top_k: int = 5, scope: str = "all") -> list[dict]:
    query_terms = set(keywords(question))
    candidates: list[dict] = []

    if scope in {"all", "knowledge"}:
        for node in db.scalars(select(KnowledgeNode)).all():
            text = "\n".join(
                [
                    node.title,
                    node.summary,
                    node.definition,
                    node.intuition,
                    node.why_it_matters,
                    node.math_form,
                    " ".join(node.tags or []),
                ]
            )
            score = score_text(query_terms, text, node.tags)
            if score > 0:
                candidates.append(
                    {
                        "score": score,
                        "source_type": "knowledge",
                        "knowledge_slug": node.slug,
                        "source_label": f"内置知识：{node.title}",
                        "content": text[:1000],
                    }
                )

    if scope in {"all", "uploads"}:
        for chunk in db.scalars(select(RagChunk)).all():
            score = score_text(query_terms, chunk.content, chunk.keywords)
            if score > 0:
                candidates.append(
                    {
                        "score": score,
                        "source_type": "upload",
                        "document_id": chunk.document_id,
                        "source_label": chunk.source_label,
                        "content": chunk.content,
                    }
                )

    return sorted(candidates, key=lambda item: item["score"], reverse=True)[:top_k]
