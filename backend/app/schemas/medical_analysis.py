from datetime import datetime

from pydantic import BaseModel, ConfigDict


class MedicalAnalysisResponse(BaseModel):
    document_id: int
    status: str
    analysis: dict
    created_at: datetime | None = None

    model_config = ConfigDict(from_attributes=True)