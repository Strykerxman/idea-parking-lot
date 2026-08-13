from app.models import Idea
from app.database import SessionLocal

def add_idea(idea: Idea) -> None:
    with SessionLocal.begin() as session:
        session.add(idea)

    return idea