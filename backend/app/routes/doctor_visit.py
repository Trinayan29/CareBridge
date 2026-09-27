import json

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.routes.auth import get_current_user
from app.models.doctor_visit import DoctorVisit
from app.models.health_timeline import HealthTimeline
from app.schemas.doctor_visit import DoctorVisitCreate, DoctorVisitResponse


router = APIRouter()


@router.post("/", response_model=DoctorVisitResponse)
def create_doctor_visit(
    visit_data: DoctorVisitCreate,
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user),
):
    user_id = current_user.id

    visit = DoctorVisit(
        user_id=user_id,
        concern=visit_data.concern,
        duration=visit_data.duration,
        severity=visit_data.severity,
        changes=visit_data.changes,
        medications=visit_data.medications,
        documents=visit_data.documents,
        questions=json.dumps(visit_data.questions),
    )

    db.add(visit)
    db.commit()
    db.refresh(visit)

    timeline_event = HealthTimeline(
        user_id=user_id,
        event_type="doctor_visit",
        title="Doctor visit summary created",
        description=f"Visit preparation created for: {visit_data.concern}",
        reference_id=visit.id,
    )

    db.add(timeline_event)
    db.commit()

    return {
        "id": visit.id,
        "user_id": visit.user_id,
        "concern": visit.concern,
        "duration": visit.duration,
        "severity": visit.severity,
        "changes": visit.changes,
        "medications": visit.medications,
        "documents": visit.documents,
        "questions": visit_data.questions,
        "created_at": visit.created_at,
        "updated_at": visit.updated_at,
    }


@router.get("/", response_model=list[DoctorVisitResponse])
def get_doctor_visits(
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user),
):
    visits = (
        db.query(DoctorVisit)
        .filter(DoctorVisit.user_id == current_user.id)
        .order_by(DoctorVisit.created_at.desc())
        .all()
    )

    return [
        {
            "id": visit.id,
            "user_id": visit.user_id,
            "concern": visit.concern,
            "duration": visit.duration,
            "severity": visit.severity,
            "changes": visit.changes,
            "medications": visit.medications,
            "documents": visit.documents,
            "questions": json.loads(visit.questions) if visit.questions else [],
            "created_at": visit.created_at,
            "updated_at": visit.updated_at,
        }
        for visit in visits
    ]
