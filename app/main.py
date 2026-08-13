from pathlib import Path

from fastapi import FastAPI, Request
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates

from app.routes import router
import app.crud as crud

BASE_DIR = Path(__file__).resolve().parent.parent

app = FastAPI()
templates = Jinja2Templates(directory=str(BASE_DIR / "templates"))

app.mount("/static", StaticFiles(directory=str(BASE_DIR / "static")), name="static")
app.include_router(router)

@app.get("/")
def home(request: Request):
    user_ideas = crud.get_all_ideas()

    return templates.TemplateResponse(
        request=request,
        name="dashboard.html",
        context={"user_ideas": user_ideas}
    )


