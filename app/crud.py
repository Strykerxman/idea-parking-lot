from sqlalchemy import select

from app.models import Idea
from app.database import SessionLocal

def add_idea(idea: Idea) -> None:
    with SessionLocal.begin() as session:
        session.add(idea)

    return idea


def get_all_ideas():
    all_ideas = None
    with SessionLocal.begin() as session:
        statement = select(Idea)
        all_ideas = session.execute(statement).all()

    return all_ideas