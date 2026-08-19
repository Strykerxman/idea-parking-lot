import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from app.database import Base, SessionLocal
from app.models import Idea

@pytest.fixture(autouse=True, scope="session")
def setup_test_db():
    """
    Creates an isolated in-memory SQLite database for the test session.
    """

    test_engine = create_engine(
        "sqlite:///:memory:",
        connect_args={"check_same_thread": False}
    )

    SessionLocal.configure(bind=test_engine)

    Base.metadata.create_all(bind=test_engine)
    yield
    Base.metadata.drop_all(bind=test_engine)


@pytest.fixture(autouse=True)
def clean_db_each_test():
    """
    Ensures each individual test starts with a completely empty database
    """

    yield
    # open a new db session each time a test is ran to delete all test db entries, commit once complete
    with SessionLocal() as session:
        session.query(Idea).delete()
        session.commit()
