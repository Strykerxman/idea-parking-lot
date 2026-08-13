from fastapi import APIRouter
from app.api.endpoints.manage_ideas import router as idea_router

router = APIRouter()

router.include_router(idea_router, tags=["Idea Parking Lot"], prefix="/ideas")

__all__ = ["router"]