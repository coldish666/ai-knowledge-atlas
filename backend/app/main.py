from fastapi import FastAPI, HTTPException
from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles
from fastapi.middleware.cors import CORSMiddleware

from app.core.config import settings
from app.db.init_db import init_db
from app.routers import graph, knowledge, rag, resources, search, settings as settings_router, tutor


def create_app() -> FastAPI:
    init_db()

    app = FastAPI(title="AI Knowledge Atlas API", version="0.1.0")
    allow_credentials = "*" not in settings.cors_origins
    app.add_middleware(
        CORSMiddleware,
        allow_origins=settings.cors_origins,
        allow_credentials=allow_credentials,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    @app.get("/health")
    def health():
        return {"status": "ok", "service": "AI Knowledge Atlas API"}

    app.include_router(knowledge.router)
    app.include_router(search.router)
    app.include_router(graph.router)
    app.include_router(resources.router)
    app.include_router(rag.router)
    app.include_router(tutor.router)
    app.include_router(settings_router.router)

    dist_dir = settings.frontend_dist_dir
    assets_dir = dist_dir / "assets"
    index_file = dist_dir / "index.html"
    if assets_dir.exists():
        app.mount("/assets", StaticFiles(directory=assets_dir), name="frontend-assets")

    @app.get("/", include_in_schema=False)
    def serve_index():
        if index_file.exists():
            return FileResponse(index_file)
        raise HTTPException(status_code=404, detail="Frontend build not found. Run `npm run build` in frontend.")

    @app.get("/{full_path:path}", include_in_schema=False)
    def serve_spa(full_path: str):
        if full_path in {"api", "health", "docs", "openapi.json", "redoc"} or full_path.startswith(("api/", "redoc/")):
            raise HTTPException(status_code=404, detail="Not found")
        if index_file.exists():
            return FileResponse(index_file)
        raise HTTPException(status_code=404, detail="Frontend build not found. Run `npm run build` in frontend.")
    return app


app = create_app()
