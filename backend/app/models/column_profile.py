from sqlalchemy import Boolean, Float, ForeignKey, Integer, String
from sqlalchemy.dialects.postgresql import JSONB
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.core.database import Base


from typing import TYPE_CHECKING

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from app.models.dataset_profile import DatasetProfile

class ColumnProfile(Base):
    __tablename__ = "column_profiles"

    id: Mapped[int] = mapped_column(primary_key=True)

    dataset_profile_id: Mapped[int] = mapped_column(
        ForeignKey("dataset_profiles.id", ondelete="CASCADE"),
        nullable=False,
        index=True,
    )

    column_name: Mapped[str] = mapped_column(
        String(255),
        nullable=False,
    )

    data_type: Mapped[str] = mapped_column(
        String(100),
        nullable=False,
    )

    total_count: Mapped[int] = mapped_column(
        Integer,
        nullable=False,
    )

    missing_count: Mapped[int] = mapped_column(
        Integer,
        nullable=False,
        default=0,
    )

    missing_percentage: Mapped[float] = mapped_column(
        Float,
        nullable=False,
        default=0.0,
    )

    distinct_count: Mapped[int] = mapped_column(
        Integer,
        nullable=False,
        default=0,
    )

    distinct_percentage: Mapped[float] = mapped_column(
        Float,
        nullable=False,
        default=0.0,
    )

    is_identifier_candidate: Mapped[bool] = mapped_column(
        Boolean,
        nullable=False,
        default=False,
    )

    statistics: Mapped[dict | None] = mapped_column(
        JSONB,
        nullable=True,
    )

    dataset_profile: Mapped["DatasetProfile"] = relationship(
        back_populates="columns",
    )