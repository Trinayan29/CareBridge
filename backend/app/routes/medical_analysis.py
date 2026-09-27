from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.core.security import decode_access_token
from app.models.medical_document import MedicalDocument
from app.services.ai_service import ai_service
from app.schemas.medical_analysis import MedicalAnalysisResponse

from app.models.health_timeline import HealthTimeline

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
    "/{document_id}",
    response_model=MedicalAnalysisResponse,
)
def analyze_medical_document(
    document_id: int,
    user_id: int = Depends(get_current_user_id),
    db: Session = Depends(get_db),
):
    document = db.get(MedicalDocument, document_id)

    if not document or document.user_id != user_id:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Medical document not found",
        )

    if not document.extracted_text:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="No extracted text is available for this document",
        )

    result = ai_service.analyze_medical_report(document.extracted_text)

    timeline_event = HealthTimeline(
        user_id=user_id,
        event_type="medical_analysis",
        title="Medical document analyzed",
        description=f"Analysis performed for: {document.original_filename}",
        reference_id=document.id,
    )

    db.add(timeline_event)
    db.commit()

    return {
        "document_id": document.id,
        "status": result["status"],
        "analysis": result,
        "created_at": document.created_at,
    }