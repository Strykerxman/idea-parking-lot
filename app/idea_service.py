from app.models import Idea, IdeaStatus
import app.crud as crud

def create_idea(title: str, description: str | None = None) -> Idea:
    clean_title = title.strip()

    if not clean_title:
        raise ValueError("Idea title cannot be empty.")

    clean_desc = (
        None
        if description is None
        else description.strip()
    )
    # description = None: user didnt add optional description to idea
    # description is not None: user added a description >> can be "" -> todo: 

    idea = Idea(
        title=clean_title,
        description=clean_desc,
        status=IdeaStatus.PARKED
    )

    crud.add_idea(idea)
    return idea
