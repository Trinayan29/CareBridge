from datetime import datetime

from pydantic import BaseModel, ConfigDict


class HealthTimelineResponse(BaseModel):
    id: int
    user_id: int
    event_type: str
    title: str
    description: str | None = None
    reference_id: int | None = None
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)