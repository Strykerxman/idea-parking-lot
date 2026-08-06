from datetime import datetime, timezone
from enum import Enum

from app.database import Base
from sqlalchemy import String, Text, Enum as SqlEnum, DateTime
from sqlalchemy.orm import Mapped, mapped_column

class IdeaStatus(str, Enum):
    ACTIVE = "active"
    PARKED = "parked"
    COMPLETED = "completed"
    DROPPED = "dropped"

# todo: migrate to SQLAlchemy ORM
class Idea(Base):
    __tablename__ = "ideas"

    id: Mapped[int] = mapped_column(primary_key=True)
    title: Mapped[str] = mapped_column(String(200), nullable=False) # not nullable to be searchable, identifiable and demonstrative (like on the webpage)
    description: Mapped[str] = mapped_column(Text, default="", nullable=False)
    
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        default_factory=lambda: datetime.now(timezone.utc), 
        nullable=False
    )
    status: Mapped[IdeaStatus] = mapped_column(default=IdeaStatus.PARKED, nullable=False)
        



