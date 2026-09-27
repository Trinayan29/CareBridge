from datetime import datetime

from sqlalchemy import DateTime, ForeignKey, String, Text
from sqlalchemy.orm import Mapped, mapped_column

from app.core.database import Base


class HealthConcern(Base):
    __tablename__ = "health_concerns"

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

    symptoms: Mapped[str | None] = mapped_column(
        Text,
        nullable=True
    )

    duration: Mapped[str | None] = mapped_column(
        String(100),
        nullable=True
    )

    severity: Mapped[str | None] = mapped_column(
        String(50),
        nullable=True
    )

    status: Mapped[str] = mapped_column(
        String(30),
        default="active",
        nullable=False
    )

    created_at: Mapped[datetime] = mapped_column(
        DateTime,
        default=datetime.utcnow,
        nullable=False
    )

    @property
    def title(self) -> str:
        return self.concern

    @property
    def description(self) -> str:
        return self.symptoms or ""

    @property
    def updated_at(self) -> datetime:
        return self.created_at