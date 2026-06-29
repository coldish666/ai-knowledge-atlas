from sqlalchemy import Boolean, Float, Integer, String
from sqlalchemy.orm import Mapped, mapped_column

from app.db.database import Base


class AppSettings(Base):
    __tablename__ = "app_settings"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, default=1)
    user_name: Mapped[str] = mapped_column(String(120), default="AI 学习者")
    preferred_style: Mapped[str] = mapped_column(String(80), default="直觉版")
    llm_provider: Mapped[str] = mapped_column(String(80), default="mock")
    api_base_url: Mapped[str] = mapped_column(String(300), default="https://api.openai.com/v1")
    ai_enabled: Mapped[bool] = mapped_column(Boolean, default=True)
    max_rag_chunks: Mapped[float] = mapped_column(Float, default=5)
