# Repository Guidelines

## Project Goal

AI Knowledge Atlas / AI学习知识索引 is a local-first interactive AI knowledge system. Its focus is knowledge content, search, relationships, graph browsing, Mock tutor explanations, and RAG Q&A. Do not steer it back into task tracking, check-ins, learning plans, or note management.

## Technology Stack

- Backend: Python 3.11+, FastAPI, SQLAlchemy, SQLite, Pydantic, pytest.
- Frontend: React, Vite, TypeScript, plain CSS.
- AI/RAG: MockLLMProvider by default, OpenAI-compatible provider interface reserved, Markdown/TXT ingestion with keyword retrieval.

## Directory Structure

- `backend/app/models/`: knowledge, RAG, and settings models.
- `backend/app/routers/`: `knowledge`, `search`, `graph`, `rag`, `tutor`, and `settings` API routes.
- `backend/app/seed/seed_knowledge.py`: built-in AI knowledge catalog and relationship generation.
- `frontend/src/pages/`: Home, KnowledgeIndex, KnowledgeDetail, GraphView, SearchPage, RagPage, TutorPage, Settings.
- `frontend/src/components/`: layout, search, cards, related panel, graph, formula, and code blocks.
- `data/uploads/`: uploaded RAG resources.
- `docs/`: product, schema, roadmap, API, and content guide.

## Development Commands

Backend:

```bash
cd backend
pip install -r requirements.txt
uvicorn app.main:app --reload
pytest
```

Frontend:

```bash
cd frontend
npm install
npm run dev
npm run build
```

## Coding Style

Keep route handlers thin and move retrieval, graph, search, and RAG behavior into services. Use `snake_case` for Python files/functions, `PascalCase` for React components, and shared TypeScript shapes in `frontend/src/types/knowledge.ts`.

## Content Rules

Every knowledge point must include real explanatory content: summary, definition, intuition, why it matters, math/formula, code, applications, misconceptions, relations, resources, and self-check questions. Empty title-only nodes are not acceptable.

## Security & Configuration

Do not commit real API keys. The app must run with the mock provider when `OPENAI_API_KEY` is absent. Put local overrides in ignored `.env` files and keep `backend/.env.example` safe.
