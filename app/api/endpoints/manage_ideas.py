from fastapi import APIRouter, HTTPException, status
from fastapi.templating import Jinja2Templates
from fastapi.responses import RedirectResponse

from app.api.schemas import IdeaCreate, IdeaResponse
from app.models import Idea
from app import idea_service as svc
from app.api import schemas

router = APIRouter()
templates = Jinja2Templates(directory="templates")

@router.post("/new", response_model=IdeaResponse, status_code=status.HTTP_201_CREATED)
def park_idea(payload: schemas.IdeaCreate):
    try:
        user_idea = IdeaCreate(title=payload.title, description=payload.description)
        svc.create_idea(user_idea)
        
        return RedirectResponse(
            url="/",
            status_code=status.HTTP_303_SEE_OTHER
        )

    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_CONTENT,
            detail=str(e)
        )