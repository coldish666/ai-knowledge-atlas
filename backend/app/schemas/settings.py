from pydantic import BaseModel, ConfigDict


class ORMModel(BaseModel):
    model_config = ConfigDict(from_attributes=True)


class SettingsRead(ORMModel):
    id: int
    user_name: str
    preferred_style: str
    llm_provider: str
    api_base_url: str
    ai_enabled: bool
    max_rag_chunks: float


class SettingsUpdate(BaseModel):
    user_name: str | None = None
    preferred_style: str | None = None
    llm_provider: str | None = None
    api_base_url: str | None = None
    ai_enabled: bool | None = None
    max_rag_chunks: float | None = None
