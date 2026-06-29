from pathlib import Path
from uuid import uuid4

from fastapi import UploadFile
from sqlalchemy.orm import Session

from app.core.config import settings
from app.models import RagChunk, RagDocument
from app.rag.chunker import chunk_text, keywords


SUPPORTED_EXTENSIONS = {".md", ".markdown", ".txt"}


async def ingest_upload(db: Session, file: UploadFile) -> tuple[RagDocument, int]:
    suffix = Path(file.filename or "resource.txt").suffix.lower()
    if suffix not in SUPPORTED_EXTENSIONS:
        raise ValueError("当前版本仅支持 Markdown / TXT 文件；PDF/PPT 解析已预留扩展。")

    settings.ensure_dirs()
    safe_name = f"{uuid4().hex}{suffix}"
    target = settings.upload_dir / safe_name
    target.write_bytes(await file.read())
    text = target.read_text(encoding="utf-8", errors="ignore")

    document = RagDocument(
        filename=safe_name,
        original_name=file.filename or safe_name,
        content_type=file.content_type or "text/plain",
        path=str(target),
    )
    db.add(document)
    db.flush()

    chunks = chunk_text(text)
    for index, chunk in enumerate(chunks):
        db.add(
            RagChunk(
                document_id=document.id,
                chunk_index=index,
                content=chunk,
                source_label=f"{document.original_name}#chunk-{index + 1}",
                keywords=keywords(chunk),
            )
        )
    db.commit()
    db.refresh(document)
    return document, len(chunks)
