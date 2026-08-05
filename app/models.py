from dataclasses import dataclass, field
from datetime import datetime
from enum import Enum, auto

class IdeaStatus(Enum):
    ACTIVE = auto()
    PARKED = auto()
    COMPLETED = auto()
    DROPPED = auto()

# todo: migrate to SQLAlchemy ORM
@dataclass
class Idea:
    title: str
    description: str
    id: int | None = None
    created_at: datetime = field(default_factory=datetime.now)
    status: IdeaStatus = IdeaStatus.PARKED
        



