from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from sqlalchemy import select
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.core.security import decode_access_token
from app.models.health_timeline import HealthTimeline
from app.schemas.health_timeline import HealthTimelineResponse

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


@router.get("/", response_model=list[HealthTimelineResponse])
def get_health_timeline(
    user_id: int = Depends(get_current_user_id),
    db: Session = Depends(get_db),
):
    timeline = db.scalars(
        select(HealthTimeline)
        .where(HealthTimeline.user_id == user_id)
        .order_by(HealthTimeline.created_at.desc())
    ).all()

    return timeline