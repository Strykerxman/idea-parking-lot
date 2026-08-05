from app.models import Idea

def create_idea(title: str, description: str | None = None) -> Idea:
    clean_title = title.strip()

    if not clean_title:
        raise ValueError("Idea title cannot be empty.")
    
    return Idea(
        title=clean_title,
        description=(description or "").strip()
    )