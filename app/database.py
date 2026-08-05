from collections.abc import Generator

from sqlalchemy import create_engine
from sqlalchemy.orm import DeclarativeBase, Session, sessionmaker

from app.config import DATABASE_URL

# engine owns the synchronous PostgreSQL connection pool.
engine = create_engine(DATABASE_URL)

# SessionLocal creates short-lived ORM sessions bound to the engine.
SessionLocal = sessionmaker(bind=engine, expire_on_commit=False)


class Base(DeclarativeBase):
    # Base gives future ORM models shared SQLAlchemy 2.x metadata.
    pass


def get_db() -> Generator[Session, None, None]:
    # FastAPI dependency: one session per request, always closed afterward.
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
