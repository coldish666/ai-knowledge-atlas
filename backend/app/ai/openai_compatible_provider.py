from app.ai.base import LLMProvider
from app.ai.mock_provider import MockLLMProvider
from app.core.config import settings


class OpenAICompatibleProvider(LLMProvider):
    name = "openai-compatible"

    def generate(self, prompt: str, context: list[str] | None = None, style: str = "直觉版") -> str:
        # TODO: Connect an OpenAI-compatible chat completion client here.
        # The first version intentionally falls back to mock output when no key is configured.
        if not settings.openai_api_key:
            return MockLLMProvider().generate(prompt, context, style)
        return (
            "OpenAI-compatible provider placeholder: a key is configured, but live calls are intentionally disabled "
            "in this local-first version. Wire the SDK call in backend/app/ai/openai_compatible_provider.py."
        )
