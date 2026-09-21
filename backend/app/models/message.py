from datetime import datetime, timezone
from typing import TYPE_CHECKING

from sqlalchemy import DateTime, ForeignKey, String, Text
from sqlalchemy.dialects.postgresql import JSONB
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.core.database import Base

if TYPE_CHECKING:
    from app.models.conversation import Conversation


class Message(Base):
    __tablename__ = "messages"

    id: Mapped[int] = mapped_column(primary_key=True)

    conversation_id: Mapped[int] = mapped_column(
        ForeignKey("conversations.id", ondelete="CASCADE"),
        nullable=False,
        index=True,
    )

    role: Mapped[str] = mapped_column(
        String(20),
        nullable=False,
    )

    content: Mapped[str] = mapped_column(
        Text,
        nullable=False,
    )

    message_metadata: Mapped[dict | None] = mapped_column(
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

    conversation: Mapped["Conversation"] = relationship(
        back_populates="messages",
    )