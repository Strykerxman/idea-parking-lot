from fastapi import FastAPI, Request
from fastapi.staticfiles import StaticFiles

from app.routes import router
from app.config import BASE_DIR
from app.dashboard import render_dashboard


app = FastAPI()

app.mount("/static", StaticFiles(directory=str(BASE_DIR / "static")), name="static")
app.include_router(router)

@app.get("/")
def home(request: Request):
    return render_dashboard(request)


