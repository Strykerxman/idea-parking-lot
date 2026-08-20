from app.models import Idea, IdeaStatus, IdeaDifficulty, IdeaHistory
from app.database import SessionLocal
import app.crud as crud
from app.api.schemas import IdeaCreate


allowed_exit_statuses = {
    IdeaStatus.PARKED,
    IdeaStatus.COMPLETED,
    IdeaStatus.DROPPED,
}


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
    
    crud.set_idea_active(id) # Not Found exception handling in database connection


def switch_active_idea(
    new_idea_id: int,
    old_idea_new_status: IdeaStatus,
    reason: str,
    difficulty: IdeaDifficulty
) -> None:
    """Atomic idea switching, happens in a single database transaction."""
    with SessionLocal.begin() as session:
        new_idea = crud.get_idea_by_id(new_idea_id, session=session)
        active_idea = crud.get_active_idea(session=session)

        if not active_idea:
            raise ValueError("There must be an active idea to swap with.")

        if not new_idea:
            raise ValueError(f"Idea with id {new_idea_id} not found.")

        if new_idea.status != IdeaStatus.PARKED:
            raise ValueError("New idea must be parked before being activated.")

        if old_idea_new_status not in allowed_exit_statuses:
            raise ValueError("Invalid status for the previous active idea.")

        cleaned_reason = reason.strip()
        if cleaned_reason == "":
            raise ValueError("Reason cannot be empty.")

        history = IdeaHistory(
            idea_id=active_idea.id,
            from_status=IdeaStatus.ACTIVE,
            to_status=old_idea_new_status,
            reason=cleaned_reason,
            difficulty=difficulty
        )

        session.add(history)

        active_idea.status = old_idea_new_status
        new_idea.status = IdeaStatus.ACTIVE
