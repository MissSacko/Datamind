from datetime import datetime, timezone
from typing import TYPE_CHECKING

from sqlalchemy import DateTime, ForeignKey, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.core.database import Base

if TYPE_CHECKING:
    from app.models.user import User
    from app.models.dataset import Dataset
    from app.models.message import Message


class Conversation(Base):
    __tablename__ = "conversations"

    id: Mapped[int] = mapped_column(primary_key=True)

    user_id: Mapped[int] = mapped_column(
        ForeignKey("users.id", ondelete="CASCADE"),
        nullable=False,
        index=True,
    )

    dataset_id: Mapped[int | None] = mapped_column(
        ForeignKey("datasets.id", ondelete="SET NULL"),
        nullable=True,
        index=True,
    )

    title: Mapped[str] = mapped_column(
        String(255),
        nullable=False,
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

    messages: Mapped[list["Message"]] = relationship(
        back_populates="conversation",
        cascade="all, delete-orphan",
    )

    user: Mapped["User"] = relationship(
        back_populates="conversations",
    )

    dataset: Mapped["Dataset | None"] = relationship(
        back_populates="conversations",
    )