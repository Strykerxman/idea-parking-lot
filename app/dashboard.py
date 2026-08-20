from fastapi import Request
from fastapi.templating import Jinja2Templates

from app import crud
from app.config import BASE_DIR
from app.models import IdeaDifficulty, IdeaStatus


templates = Jinja2Templates(directory=str(BASE_DIR / "templates"))

def render_dashboard(
    request: Request,
    *,
    error: str | None = None,
    status_code: int = 200
):
    active_idea = crud.get_active_idea()
    parked_ideas = crud.get_parked_ideas()

    return templates.TemplateResponse(
            request=request,
            name="dashboard.html",
            context={"active_idea": active_idea,
                     "parked_ideas": parked_ideas,
                     "error" : error,
                     "IdeaStatus": IdeaStatus,
                     "IdeaDifficulty": IdeaDifficulty},
            status_code=status_code
    )