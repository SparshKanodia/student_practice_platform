from fastapi import FastAPI
from fastapi.responses import RedirectResponse
from fastapi.templating import Jinja2Templates

from app import database
from app.auth import configure_templates, router as auth_router

app = FastAPI()
templates = Jinja2Templates(directory="app/templates")
configure_templates(templates)
app.include_router(auth_router)


@app.on_event("startup")
def startup_event() -> None:
    database.create_tables()


@app.get("/")
def read_root() -> RedirectResponse:
    return RedirectResponse(url="/login", status_code=303)
