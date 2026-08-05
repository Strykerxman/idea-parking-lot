from dataclasses import dataclass, field
from datetime import datetime, timezone
from enum import Enum

class IdeaStatus(Enum):
    ACTIVE = "active"
    PARKED = "parked"
    COMPLETED = "completed"
    DROPPED = "dropped"

# todo: migrate to SQLAlchemy ORM
@dataclass
class Idea:
    title: str
    description: str
    id: int | None = None
    created_at: datetime = field(default_factory=lambda: datetime.now(timezone.utc))
    status: IdeaStatus = IdeaStatus.PARKED
        



