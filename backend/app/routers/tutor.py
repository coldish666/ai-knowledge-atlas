from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.ai import get_llm_provider
from app.db.database import get_db
from app.schemas.tutor import (
    TutorCodeExampleRequest,
    TutorCompareRequest,
    TutorExplainRequest,
    TutorResponse,
    TutorSelfCheckRequest,
)
from app.services.knowledge_service import get_by_slug
from app.services.search_service import search

router = APIRouter(prefix="/api/tutor", tags=["tutor"])


@router.post("/explain", response_model=TutorResponse)
def explain(payload: TutorExplainRequest, db: Session = Depends(get_db)):
    matches = search(db, q=payload.topic)[:3]
    context = [f"{item['title']}：{item['summary']}" for item in matches]
    provider = get_llm_provider()
    return {
        "answer": provider.generate(f"解释知识点：{payload.topic}", context=context, style=payload.style),
        "provider": provider.name,
        "references": [item["slug"] for item in matches],
    }


@router.post("/compare", response_model=TutorResponse)
def compare(payload: TutorCompareRequest, db: Session = Depends(get_db)):
    left = search(db, q=payload.left)[:1]
    right = search(db, q=payload.right)[:1]
    context = [str(item) for item in left + right]
    provider = get_llm_provider()
    return {
        "answer": provider.generate(f"比较 {payload.left} 和 {payload.right}", context=context, style=payload.style),
        "provider": provider.name,
        "references": [item["slug"] for item in left + right],
    }


@router.post("/code-example", response_model=TutorResponse)
def code_example(payload: TutorCodeExampleRequest, db: Session = Depends(get_db)):
    matches = search(db, q=payload.topic)[:1]
    if not matches:
        raise HTTPException(status_code=404, detail="No matching knowledge topic")
    node = get_by_slug(db, matches[0]["slug"])
    provider = get_llm_provider()
    return {
        "answer": provider.generate(
            f"给出 {payload.topic} 的 {payload.language} 最小代码示例",
            context=[node.code_example if node else ""],
            style="代码版",
        ),
        "provider": provider.name,
        "references": [matches[0]["slug"]],
    }


@router.post("/self-check", response_model=TutorResponse)
def self_check(payload: TutorSelfCheckRequest, db: Session = Depends(get_db)):
    matches = search(db, q=payload.topic)[:1]
    node = get_by_slug(db, matches[0]["slug"]) if matches else None
    questions = node.self_check_questions if node else [f"请解释 {payload.topic} 的定义、直觉和应用。"]
    provider = get_llm_provider()
    return {
        "answer": provider.generate(
            f"生成 {payload.difficulty} 难度自测题：{payload.topic}",
            context=questions,
            style="考试版",
        ),
        "provider": provider.name,
        "references": [node.slug] if node else [],
    }
