from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from sqlalchemy import select
from sqlalchemy.orm import Session
from app.models.health_timeline import HealthTimeline
from app.core.database import get_db
from app.core.security import decode_access_token
from app.models.health_concern import HealthConcern
from app.services.ai_service import ai_service
from app.services.safety_service import check_safety
from app.schemas.health_guidance import HealthGuidanceResponse


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


@router.post(
    "/{concern_id}",
    response_model=HealthGuidanceResponse,
)
def get_health_guidance(
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

    safety_result = check_safety(
        concern.title,
        concern.description,
    )

    if safety_result["is_emergency"]:
        return {
            "concern_id": concern.id,
            "title": concern.title,
            "safety": safety_result,
            "guidance": safety_result["message"],
            "follow_up_questions": [],
        }

    ai_result = ai_service.analyze_health_concern(
    concern.title,
    concern.description
    )
    timeline_event = HealthTimeline(
        user_id=user_id,
        event_type="health_guidance",
        title="Health guidance generated",
        description=f"Guidance generated for: {concern.title}",
        reference_id=concern.id,
    )

    db.add(timeline_event)
    db.commit()

    return {
        "concern_id": concern.id,
        "title": concern.title,
        "safety": safety_result,
        "guidance": ai_result["guidance"],
        "follow_up_questions": ai_result["follow_up_questions"],
    }