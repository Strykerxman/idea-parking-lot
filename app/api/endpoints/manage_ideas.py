from typing import Annotated
from fastapi import APIRouter, HTTPException, status, Form, Request
from fastapi.templating import Jinja2Templates
from fastapi.responses import RedirectResponse

from app.dashboard import render_dashboard
from app.api.schemas import IdeaCreate, IdeaResponse
from app.models import IdeaDifficulty, IdeaStatus
from app import idea_service as svc
from app.api import schemas

router = APIRouter()
templates = Jinja2Templates(directory="templates")

@router.post("/new", response_model=IdeaResponse, status_code=status.HTTP_201_CREATED)
def park_idea(payload: Annotated[schemas.IdeaCreate, Form()]):
    try:
        user_idea = IdeaCreate(title=payload.title, description=payload.description)
        svc.create_idea(user_idea)

    except ValueError as e:
            raise HTTPException(
                status_code=422,
                detail=str(e)
            )  
    
    return RedirectResponse(
        url="/",
        status_code=303
    )
    

@router.post("/activate/{idea_id}")
def activate_idea(request: Request, idea_id: int):
    try:
        svc.activate_idea(id=idea_id)

    except ValueError as e:
        if "not found" in str(e):
            return render_dashboard(
                request,
                error=str(e),
                status_code=404
            )

        if "already active" in str(e):
            return render_dashboard(
                request,
                error=str(e),
                status_code=409
            )

        raise

    return RedirectResponse(
        url="/",
        status_code=303
    )


@router.post("/switch/{idea_id}")
def switch_idea(
    request: Request,
    idea_id: int,
    old_idea_new_status: Annotated[IdeaStatus, Form()],
    reason: Annotated[str, Form()],
    difficulty: Annotated[IdeaDifficulty, Form()],
):
    try:
        svc.switch_active_idea(
            new_idea_id=idea_id,
            old_idea_new_status=old_idea_new_status,
            reason=reason,
            difficulty=difficulty,
        )
    except ValueError as error:
        error_message = str(error)
        error_status = (
            status.HTTP_404_NOT_FOUND
            if "not found" in error_message
            else status.HTTP_409_CONFLICT
        )
        return render_dashboard(
            request,
            error=error_message,
            status_code=error_status,
        )

    return RedirectResponse(
        url="/",
        status_code=303,
    )