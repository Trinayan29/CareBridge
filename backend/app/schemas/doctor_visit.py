from datetime import datetime
from app.routes.auth import get_current_user
from pydantic import BaseModel, ConfigDict


class DoctorVisitCreate(BaseModel):
    concern: str
    duration: str
    severity: int
    changes: str
    medications: str | None = None
    documents: str | None = None
    questions: list[str] = []


class DoctorVisitResponse(BaseModel):
    id: int
    user_id: int
    concern: str
    duration: str
    severity: int
    changes: str
    medications: str | None = None
    documents: str | None = None
    questions: list[str] = []
    created_at: datetime
    updated_at: datetime

    model_config = ConfigDict(from_attributes=True)
