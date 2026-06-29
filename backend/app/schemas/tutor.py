from pydantic import BaseModel


class TutorExplainRequest(BaseModel):
    topic: str
    style: str = "直觉版"


class TutorCompareRequest(BaseModel):
    left: str
    right: str
    style: str = "直觉版"


class TutorCodeExampleRequest(BaseModel):
    topic: str
    language: str = "python"


class TutorSelfCheckRequest(BaseModel):
    topic: str
    difficulty: str = "入门"


class TutorResponse(BaseModel):
    answer: str
    provider: str = "mock"
    references: list[str] = []
