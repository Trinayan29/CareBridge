from datetime import datetime

from sqlalchemy import DateTime, ForeignKey, Integer, String, Text
from sqlalchemy.orm import Mapped, mapped_column

from app.core.database import Base


class DoctorVisit(Base):
    __tablename__ = "doctor_visits"

    id: Mapped[int] = mapped_column(
        primary_key=True,
        index=True
    )

    user_id: Mapped[int] = mapped_column(
        ForeignKey("users.id", ondelete="CASCADE"),
        nullable=False,
        index=True
    )

    concern: Mapped[str] = mapped_column(
        Text,
        nullable=False
    )

    duration: Mapped[str] = mapped_column(
        String(100),
        nullable=False
    )

    severity: Mapped[int] = mapped_column(
        Integer,
        nullable=False
    )

    changes: Mapped[str] = mapped_column(
        Text,
        nullable=False
    )

    medications: Mapped[str | None] = mapped_column(
        Text,
        nullable=True
    )

    documents: Mapped[str | None] = mapped_column(
        Text,
        nullable=True
    )

    questions: Mapped[str | None] = mapped_column(
        Text,
        nullable=True
    )

    created_at: Mapped[datetime] = mapped_column(
        DateTime,
        default=datetime.utcnow,
        nullable=False
    )

    updated_at: Mapped[datetime] = mapped_column(
        DateTime,
        default=datetime.utcnow,
        onupdate=datetime.utcnow,
        nullable=False
    )
