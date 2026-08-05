from __future__ import annotations

import os
from pathlib import Path

from dotenv import load_dotenv

ROOT_DIR = Path(__file__).resolve().parents[1]

# Load local development variables without overriding the real environment.
load_dotenv(ROOT_DIR / ".env")

_database_url = os.getenv("DATABASE_URL")
if not _database_url:
    raise RuntimeError("DATABASE_URL is required; copy .env.example to .env or export it.")

# DATABASE_URL is the single PostgreSQL connection string used by SQLAlchemy.
DATABASE_URL: str = _database_url
