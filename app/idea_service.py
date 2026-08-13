from app.models import Idea, IdeaStatus
import app.crud as crud
from app.api.schemas import IdeaCreate

def create_idea(payload: IdeaCreate) -> Idea:
    """
    Returns the created idea database entry.
    """
    
    idea = Idea(
        title=payload.title,
        description=payload.description,
        status=IdeaStatus.PARKED
    )

    return crud.add_idea(idea)
