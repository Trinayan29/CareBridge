from datetime import datetime

from pydantic import BaseModel, ConfigDict



class HealthConcernCreate(BaseModel):
    title: str
    description: str


class HealthConcernResponse(BaseModel):
    id: int
    user_id: int
    title: str
    description: str
    status: str
    created_at: datetime
    updated_at: datetime

    model_config = ConfigDict(from_attributes=True)