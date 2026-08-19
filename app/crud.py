from sqlalchemy import Sequence, select

from app.models import Idea, IdeaStatus
from app.database import SessionLocal

def add_idea(idea: Idea) -> Idea:
    # Automatically Opens -> Begins -> Commits -> Closes
    with SessionLocal.begin() as session:
        session.add(idea)

    return idea


def get_idea_by_id(idea_id: int) -> Idea | None:
    with SessionLocal() as session:
        idea = session.get(Idea, idea_id)

    return idea


def get_all_ideas() -> Sequence[Idea]:
    # Automatically Opens -> No commit needed -> Closes
    with SessionLocal() as session:
        all_ideas = session.scalars(select(Idea)).all()

    return all_ideas


def get_active_idea() -> Idea | None:
    with SessionLocal() as session:
        idea = session.scalar(
            select(Idea).where(Idea.status == IdeaStatus.ACTIVE)
        )

    return idea


def get_parked_ideas() -> Sequence[Idea] | None:
    with SessionLocal() as session:
        parked_ideas = session.scalars(
            select(Idea).where(Idea.status == IdeaStatus.PARKED).order_by(Idea.created_at.desc())
        ).all()

    return parked_ideas


def set_idea_active(idea_id: int) -> None:
    with SessionLocal.begin() as session:
        idea = session.get(Idea, idea_id)
        if idea is None:
            raise ValueError(f"Idea with id {idea_id} not found.")

        idea.status = IdeaStatus.ACTIVE
        