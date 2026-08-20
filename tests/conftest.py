import pytest
from sqlalchemy import create_engine
from sqlalchemy.pool import StaticPool

from app.database import Base, SessionLocal
from app.models import Idea, IdeaHistory

@pytest.fixture(autouse=True, scope="session")
def setup_test_db():
    """
    Creates an isolated in-memory SQLite database for the test session.
    """

    test_engine = create_engine(
        "sqlite:///:memory:",
        connect_args={"check_same_thread": False},
        poolclass=StaticPool,
    )

    SessionLocal.configure(bind=test_engine)

    Base.metadata.create_all(bind=test_engine)
    yield
    Base.metadata.drop_all(bind=test_engine)


@pytest.fixture(autouse=True)
def clean_db_each_test():
    """Each test starts and ends with an empty database."""

    def clear_database():
        with SessionLocal.begin() as session:
            session.query(IdeaHistory).delete()
            session.query(Idea).delete()

    clear_database()

    yield

    clear_database()
