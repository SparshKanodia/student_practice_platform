import json

from fastapi import FastAPI, Request
from fastapi.responses import RedirectResponse
from fastapi.templating import Jinja2Templates

from app import database
from app.auth import configure_templates, get_current_user, router as auth_router
from app.models import update_user_progress
from app.quiz_engine import generate_placeholder_questions, select_adaptive_topics
from app.skill_engine import calculate_level, update_skill_score

app = FastAPI()
templates = Jinja2Templates(directory="app/templates")
configure_templates(templates)
app.include_router(auth_router)


@app.on_event("startup")
def startup_event() -> None:
    database.create_tables()


@app.get("/")
def read_root(request: Request) -> RedirectResponse:
    user = get_current_user(request)
    if user and user["role"] == "student":
        return RedirectResponse(url="/student", status_code=303)
    if user and user["role"] == "teacher":
        return RedirectResponse(url="/teacher", status_code=303)
    return RedirectResponse(url="/login", status_code=303)
