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


def activate_idea(id: int) -> None:
    """
    Activates an idea. Only allowed if no other ideas are active (IdeaStatus.ACTIVE).
    """
    if crud.get_active_idea() is not None:
        raise ValueError("Another idea is already active.")
    
    crud.set_idea_active(id)
