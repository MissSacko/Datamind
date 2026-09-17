from datetime import datetime, timezone

from sqlalchemy import DateTime, ForeignKey, Integer
from sqlalchemy.dialects.postgresql import JSONB
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.core.database import Base

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from app.models.column_profile import ColumnProfile

class DatasetProfile(Base):
    __tablename__ = "dataset_profiles"

    id: Mapped[int] = mapped_column(primary_key=True)

    dataset_id: Mapped[int] = mapped_column(
        ForeignKey("datasets.id", ondelete="CASCADE"),
        unique=True,
        nullable=False,
        index=True,
    )

    row_count: Mapped[int] = mapped_column(
        Integer,
        nullable=False,
    )

    column_count: Mapped[int] = mapped_column(
        Integer,
        nullable=False,
    )

    missing_value_count: Mapped[int] = mapped_column(
        Integer,
        nullable=False,
        default=0,
    )

    duplicate_row_count: Mapped[int] = mapped_column(
        Integer,
        nullable=False,
        default=0,
    )

    quality_score: Mapped[float | None] = mapped_column(
        nullable=True,
    )

    details: Mapped[dict | None] = mapped_column(
    JSONB,
    nullable=True,
    )

    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        default=lambda: datetime.now(timezone.utc),
        nullable=False,
    )

    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        default=lambda: datetime.now(timezone.utc),
        onupdate=lambda: datetime.now(timezone.utc),
        nullable=False,
    )

    columns: Mapped[list["ColumnProfile"]] = relationship(
        back_populates="dataset_profile",
        cascade="all, delete-orphan",
    )