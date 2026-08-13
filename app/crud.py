from sqlalchemy import select

from app.models import Idea
from app.database import SessionLocal

def add_idea(idea: Idea) -> None:
    with SessionLocal.begin() as session:
        session.add(idea)

    return idea


def get_all_ideas():
    with SessionLocal() as session:
        all_ideas = session.scalars(select(Idea)).all()

    return all_ideas