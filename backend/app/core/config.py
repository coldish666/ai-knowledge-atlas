from os import getenv
from pathlib import Path

from dotenv import load_dotenv


REPO_ROOT = Path(__file__).resolve().parents[3]
load_dotenv(REPO_ROOT / "backend" / ".env")
load_dotenv(REPO_ROOT / ".env")


class Settings:
    app_name = "AI Knowledge Atlas"
    repo_root = REPO_ROOT
    data_dir = Path(getenv("DATA_DIR", repo_root / "data"))
    upload_dir = Path(getenv("UPLOAD_DIR", data_dir / "uploads"))
    frontend_dist_dir = Path(getenv("FRONTEND_DIST_DIR", repo_root / "frontend" / "dist"))
    raw_database_url = getenv("DATABASE_URL")
    database_url = raw_database_url or f"sqlite:///{(data_dir / 'knowledge_atlas.db').as_posix()}"
    if database_url.startswith("postgres://"):
        database_url = database_url.replace("postgres://", "postgresql+psycopg://", 1)
    elif database_url.startswith("postgresql://") and "+psycopg" not in database_url:
        database_url = database_url.replace("postgresql://", "postgresql+psycopg://", 1)
    cors_origins = [
        origin.strip()
        for origin in getenv("CORS_ORIGINS", "http://localhost:5173,http://127.0.0.1:5173").split(",")
        if origin.strip()
    ]
    llm_provider = getenv("LLM_PROVIDER", "mock")
    openai_api_key = getenv("OPENAI_API_KEY")
    openai_base_url = getenv("OPENAI_BASE_URL", "https://api.openai.com/v1")

    def ensure_dirs(self) -> None:
        self.data_dir.mkdir(parents=True, exist_ok=True)
        self.upload_dir.mkdir(parents=True, exist_ok=True)


settings = Settings()
