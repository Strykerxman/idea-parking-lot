from typing import Annotated
from fastapi import APIRouter, HTTPException, status, Form
from fastapi.templating import Jinja2Templates
from fastapi.responses import RedirectResponse

from app.api.schemas import IdeaCreate, IdeaResponse
from app import idea_service as svc
from app.api import schemas

router = APIRouter()
templates = Jinja2Templates(directory="templates")

@router.post("/new", response_model=IdeaResponse, status_code=status.HTTP_201_CREATED)
def park_idea(payload: Annotated[schemas.IdeaCreate, Form()]):
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
    

@router.post("/activate/{idea_id}")
def activate_idea(idea_id: int):
    try:
        svc.activate_idea(id=idea_id)

        return RedirectResponse(
            url="/",
            status_code=status.HTTP_303_SEE_OTHER
        )

    except ValueError as e:
        if "not found" in str(e):
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=str(e)
            )

        if "already active" in str(e):
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail=str(e)
            )

        raise