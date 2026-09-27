from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from sqlalchemy import select
from sqlalchemy.orm import Session
from app.models.health_timeline import HealthTimeline
from app.core.database import get_db
from app.core.security import decode_access_token
from app.models.health_concern import HealthConcern
from app.schemas.health_concern import (
    HealthConcernCreate,
    HealthConcernResponse,
)
from app.services.safety_service import check_safety


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


# REPLACE YOUR OLD create_health_concern() WITH THIS
@router.post(
    "/",
    response_model=HealthConcernResponse,
    status_code=status.HTTP_201_CREATED,
)
def create_health_concern(
    concern_data: HealthConcernCreate,
    user_id: int = Depends(get_current_user_id),
    db: Session = Depends(get_db),
):
    safety_result = check_safety(
        concern_data.title,
        concern_data.description,
    )

    concern = HealthConcern(
        user_id=user_id,
        concern=concern_data.title,
        symptoms=concern_data.description,
        status="emergency" if safety_result["is_emergency"] else "active",
    )

    db.add(concern)
    db.commit()
    db.refresh(concern)

    timeline_event = HealthTimeline(
    user_id=user_id,
    event_type="health_concern",
    title=concern.title,
    description=concern.description,
    reference_id=concern.id,
    )
    db.add(timeline_event)
    db.commit()

    return concern


@router.get(
    "/",
    response_model=list[HealthConcernResponse],
)
def get_health_concerns(
    user_id: int = Depends(get_current_user_id),
    db: Session = Depends(get_db),
):
    concerns = db.scalars(
        select(HealthConcern)
        .where(HealthConcern.user_id == user_id)
        .order_by(HealthConcern.created_at.desc())
    ).all()

    return concerns


@router.get(
    "/{concern_id}",
    response_model=HealthConcernResponse,
)
def get_health_concern(
    concern_id: int,
    user_id: int = Depends(get_current_user_id),
    db: Session = Depends(get_db),
):
    concern = db.scalar(
        select(HealthConcern).where(
            HealthConcern.id == concern_id,
            HealthConcern.user_id == user_id,
        )
    )

    if not concern:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Health concern not found",
        )

    return concern