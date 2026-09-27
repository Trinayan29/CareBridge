from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from sqlalchemy import select
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.core.security import decode_access_token
from app.models.health_profile import HealthProfile
from app.schemas.health_profile import (
    HealthProfileCreate,
    HealthProfileResponse,
)

router = APIRouter()
security = HTTPBearer()


def get_current_user_id(
    credentials: HTTPAuthorizationCredentials = Depends(security),
) -> int:
    try:
        return decode_access_token(credentials.credentials)
    except Exception:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid or expired token",
        )


@router.get(
    "/",
    response_model=HealthProfileResponse,
)
def get_health_profile(
    user_id: int = Depends(get_current_user_id),
    db: Session = Depends(get_db),
):
    profile = db.scalar(
        select(HealthProfile).where(
            HealthProfile.user_id == user_id
        )
    )

    if not profile:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Health profile not found",
        )

    return profile


@router.put(
    "/",
    response_model=HealthProfileResponse,
)
def create_or_update_health_profile(
    profile_data: HealthProfileCreate,
    user_id: int = Depends(get_current_user_id),
    db: Session = Depends(get_db),
):
    profile = db.scalar(
        select(HealthProfile).where(
            HealthProfile.user_id == user_id
        )
    )

    if profile:
        profile.date_of_birth = profile_data.date_of_birth
        profile.blood_group = profile_data.blood_group
        profile.allergies = profile_data.allergies
        profile.medical_conditions = profile_data.medical_conditions
        profile.current_medications = profile_data.current_medications
        profile.emergency_contact_name = profile_data.emergency_contact_name
        profile.emergency_contact_phone = profile_data.emergency_contact_phone
    else:
        profile = HealthProfile(
            user_id=user_id,
            date_of_birth=profile_data.date_of_birth,
            blood_group=profile_data.blood_group,
            allergies=profile_data.allergies,
            medical_conditions=profile_data.medical_conditions,
            current_medications=profile_data.current_medications,
            emergency_contact_name=profile_data.emergency_contact_name,
            emergency_contact_phone=profile_data.emergency_contact_phone,
        )

        db.add(profile)

    db.commit()
    db.refresh(profile)

    return profile