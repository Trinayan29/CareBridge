from datetime import date, datetime

from pydantic import BaseModel, ConfigDict


class HealthProfileBase(BaseModel):
    date_of_birth: date | None = None
    blood_group: str | None = None
    allergies: str | None = None
    medical_conditions: str | None = None
    current_medications: str | None = None
    emergency_contact_name: str | None = None
    emergency_contact_phone: str | None = None


class HealthProfileCreate(HealthProfileBase):
    pass


class HealthProfileResponse(HealthProfileBase):
    id: int
    user_id: int
    created_at: datetime
    updated_at: datetime

    model_config = ConfigDict(from_attributes=True)