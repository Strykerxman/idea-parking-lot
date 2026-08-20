from pydantic import BaseModel, Field, field_validator
from datetime import datetime

from app.models import IdeaStatus


class IdeaCreate(BaseModel):
    title: str = Field(max_length=200, description="Give your idea a name!")
    description: str | None = None

    @field_validator("title", mode="after") # happens AFTER pydantic type check (str)
    def sanitize_and_validate_title(value: str) -> str:
        cleaned = value.strip()
        if cleaned == "":
            raise ValueError("Idea title cannot be empty.")
        return cleaned

    @field_validator("description", mode="before") # happens BEFORE pydantic type
    def validate_and_sanitize_desc(value: str | None) -> str | None:
        if value is None:
            return None
        cleaned = value.strip()
        return cleaned if cleaned != "" else None


class IdeaResponse(BaseModel):
    id: int
    title: str
    description: str | None
    status: IdeaStatus
    created_at: datetime
