from pathlib import Path
from uuid import uuid4

from fastapi import (
    APIRouter,
    Depends,
    HTTPException,
    status,
    UploadFile,
    File,
)
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from sqlalchemy import select
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.core.security import decode_access_token
from app.models.medical_document import MedicalDocument
from app.services.document_processor import extract_text_from_document
from app.models.health_timeline import HealthTimeline


router = APIRouter()
security = HTTPBearer()

UPLOAD_DIR = Path("uploads")
UPLOAD_DIR.mkdir(exist_ok=True)

ALLOWED_EXTENSIONS = {
    ".pdf",
    ".png",
    ".jpg",
    ".jpeg",
}


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
    "/upload",
    status_code=status.HTTP_201_CREATED,
)
async def upload_medical_document(
    file: UploadFile = File(...),
    user_id: int = Depends(get_current_user_id),
    db: Session = Depends(get_db),
):
    if not file.filename:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Filename is required",
        )

    extension = Path(file.filename).suffix.lower()

    if extension not in ALLOWED_EXTENSIONS:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Only PDF, PNG, JPG and JPEG files are allowed",
        )

    safe_filename = f"{uuid4().hex}{extension}"
    file_path = UPLOAD_DIR / safe_filename

    contents = await file.read()
    file_path.write_bytes(contents)

    document = MedicalDocument(
        user_id=user_id,
        original_filename=file.filename,
        document_type="other",
        file_path=str(file_path),
        processing_status="processing",
    )

    db.add(document)
    db.commit()
    db.refresh(document)

    try:
        extracted_text = extract_text_from_document(
            str(file_path),
            extension,
        )

        if extracted_text:
            document.extracted_text = extracted_text
            document.processing_status = "completed"
        else:
            document.processing_status = "pending"

    except Exception:
        document.processing_status = "failed"

    db.commit()
    db.refresh(document)
    timeline_event = HealthTimeline(
        user_id=user_id,
        event_type="medical_document",
        title="Medical document uploaded",
        description=f"Uploaded document: {document.original_filename}",
        reference_id=document.id,
    )

    db.add(timeline_event)
    db.commit()

    return {
    "message": "Medical document uploaded successfully",
    "document_id": document.id,
    "filename": document.original_filename,
    "processing_status": document.processing_status,
    }


@router.get("/")
def get_medical_documents(
    user_id: int = Depends(get_current_user_id),
    db: Session = Depends(get_db),
):
    documents = db.scalars(
        select(MedicalDocument)
        .where(MedicalDocument.user_id == user_id)
        .order_by(MedicalDocument.created_at.desc())
    ).all()

    return documents