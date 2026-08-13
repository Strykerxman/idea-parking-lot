from pathlib import Path

from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates

from app.routes import router

BASE_DIR = Path(__file__).resolve().parent.parent

app = FastAPI()
templates = Jinja2Templates(directory=str(BASE_DIR / "templates"))

app.mount("/static", StaticFiles(directory=str(BASE_DIR / "static")), name="static")
app.include_router(router)

@app.get("/")
def root():
    return {"message": "Welcome to your idea parking lot, anything came up to mind?"}


