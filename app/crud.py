from sqlalchemy import Sequence, select
from sqlalchemy.orm import Session

from app.models import Idea, IdeaStatus, IdeaHistory
from app.database import SessionLocal


def add_idea(idea: Idea) -> Idea:
    # Automatically Opens -> Begins -> Commits -> Closes
    with SessionLocal.begin() as session:
        session.add(idea)

    return idea


def get_idea_by_id(idea_id: int, session: Session | None = None) -> Idea | None:
    if session is not None:
        return session.get(Idea, idea_id)

    with SessionLocal() as owned_session:
        idea = owned_session.get(Idea, idea_id)

    return idea


def get_all_ideas() -> Sequence[Idea]:
    # Automatically Opens -> No commit needed -> Closes
    with SessionLocal() as session:
        all_ideas = session.scalars(select(Idea)).all()

    return all_ideas


def get_active_idea(session: Session | None = None) -> Idea | None:
    statement = select(Idea).where(Idea.status == IdeaStatus.ACTIVE)

    if session is not None:
        return session.scalar(statement)

    with SessionLocal() as owned_session:
        idea = owned_session.scalar(statement)

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


def set_idea_status(idea_id: int, new_status: IdeaStatus):
    with SessionLocal.begin() as session:
        idea = session.get(Idea, idea_id)
        if idea is None:
            raise ValueError(f"Idea with id {idea_id} not found.")

        idea.status == new_status


def get_idea_history(idea_id: int) -> IdeaHistory:
    with SessionLocal() as session:
        return session.scalars(
                select(IdeaHistory)
                .where(IdeaHistory.idea_id == idea_id)
                .order_by(IdeaHistory.created_at)
            ).all()