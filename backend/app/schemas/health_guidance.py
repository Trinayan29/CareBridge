from pydantic import BaseModel


class SafetyResult(BaseModel):
    is_emergency: bool
    matched_keywords: list[str]
    message: str


class HealthGuidanceResponse(BaseModel):
    concern_id: int
    title: str
    safety: SafetyResult
    guidance: str
    follow_up_questions: list[str]