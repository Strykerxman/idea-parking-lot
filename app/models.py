from datetime import datetime
from enum import Enum

from app.database import Base
from sqlalchemy import String, Text, Enum as SqlEnum, DateTime, func, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column


class IdeaDifficulty(str, Enum):
    TOO_EASY = "too_easy"
    JUST_RIGHT = "just_right"
    TOO_HARD = "too_hard"


class IdeaStatus(str, Enum):
    ACTIVE = "active"
    PARKED = "parked" # maybe later
    COMPLETED = "completed"
    DROPPED = "dropped" # consciously stopped


class Idea(Base):
    __tablename__ = "ideas"
    __mapper_args__ = {"eager_defaults": True}

    id: Mapped[int] = mapped_column(primary_key=True)
    title: Mapped[str] = mapped_column(String(200), nullable=False) # not nullable to be searchable, identifiable and demonstrative (like on the webpage)
    description: Mapped[str | None] = mapped_column(Text, nullable=True) # we allow description to be None
    
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        server_default=func.now(), 
        nullable=False
    )

    status: Mapped[IdeaStatus] = mapped_column(
        SqlEnum(IdeaStatus, name="idea_status"), 
        default=IdeaStatus.PARKED,
        nullable=False
    )


class IdeaHistory(Base):
    __tablename__ = "idea_history"

    id: Mapped[int] = mapped_column(primary_key=True)
    idea_id: Mapped[int] = mapped_column(ForeignKey("ideas.id"))

    from_status: Mapped[IdeaStatus] = mapped_column(SqlEnum(IdeaStatus, name="from_status"))
    to_status: Mapped[IdeaStatus] = mapped_column(SqlEnum(IdeaStatus, name="to_status"))

    reason: Mapped[str] = mapped_column(Text)
    difficulty: Mapped[IdeaDifficulty] = mapped_column(SqlEnum(IdeaDifficulty, name="difficulty"))

    created_at: Mapped[datetime] = mapped_column(
            DateTime(timezone=True),
            server_default=func.now(), 
            nullable=False
    )