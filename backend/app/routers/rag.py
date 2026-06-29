from fastapi import APIRouter, Depends, File, HTTPException, UploadFile
from sqlalchemy import select
from sqlalchemy.orm import Session

from app.ai import get_llm_provider
from app.db.database import get_db
from app.models import RagDocument
from app.rag import ingest_upload, retrieve
from app.schemas.rag import RagAskRequest, RagAskResponse, RagDocumentRead, RagUploadResponse

router = APIRouter(prefix="/api/rag", tags=["rag"])


@router.post("/upload", response_model=RagUploadResponse)
async def upload_resource(file: UploadFile = File(...), db: Session = Depends(get_db)):
    try:
        document, chunk_count = await ingest_upload(db, file)
    except ValueError as exc:
        raise HTTPException(status_code=400, detail=str(exc)) from exc
    return {
        "id": document.id,
        "original_name": document.original_name,
        "chunks": chunk_count,
    }


@router.post("/ask", response_model=RagAskResponse)
def ask(payload: RagAskRequest, db: Session = Depends(get_db)):
    chunks = retrieve(db, payload.question, payload.top_k, payload.scope)
    provider = get_llm_provider()
    answer = provider.generate(
        f"请基于引用片段回答：{payload.question}",
        context=[chunk["content"] for chunk in chunks],
        style="项目应用版",
    )
    return {
        "answer": answer,
        "citations": [
            {
                "source_label": chunk["source_label"],
                "content": chunk["content"],
                "source_type": chunk["source_type"],
                "document_id": chunk.get("document_id"),
                "knowledge_slug": chunk.get("knowledge_slug"),
            }
            for chunk in chunks
        ],
    }


@router.get("/documents", response_model=list[RagDocumentRead])
def read_documents(db: Session = Depends(get_db)):
    return list(db.scalars(select(RagDocument).order_by(RagDocument.uploaded_at.desc())).all())
