from app.ai.base import LLMProvider
from app.ai.mock_provider import MockLLMProvider
from app.ai.openai_compatible_provider import OpenAICompatibleProvider
from app.core.config import settings


def get_llm_provider(provider_name: str | None = None) -> LLMProvider:
    name = provider_name or settings.llm_provider
    if name == "openai-compatible":
        return OpenAICompatibleProvider()
    return MockLLMProvider()
