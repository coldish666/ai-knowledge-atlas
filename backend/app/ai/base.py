from abc import ABC, abstractmethod


class LLMProvider(ABC):
    name: str

    @abstractmethod
    def generate(self, prompt: str, context: list[str] | None = None, style: str = "直觉版") -> str:
        raise NotImplementedError
