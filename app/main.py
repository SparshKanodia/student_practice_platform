import json

from fastapi import FastAPI, Request
from fastapi.responses import RedirectResponse
from fastapi.templating import Jinja2Templates

from app import database
from app.auth import get_current_user, router as auth_router
from app.models import update_user_progress
from app.quiz_engine import generate_placeholder_questions, select_adaptive_topics
from app.skill_engine import calculate_level, update_skill_score

app = FastAPI()
app.include_router(auth_router)
templates = Jinja2Templates(directory="app/templates")


@app.on_event("startup")
def startup_event() -> None:
    database.create_tables()


@app.get("/")
def read_root() -> RedirectResponse:
    return RedirectResponse(url="/login", status_code=303)


@app.get("/start-quiz")
def start_quiz(request: Request):
    user = get_current_user(request)
    if not user or user["role"] != "student":
        return RedirectResponse(url="/login", status_code=303)

    skills = json.loads(user["skills"] or "{}")
    topics = select_adaptive_topics(skills)
    questions = generate_placeholder_questions(topics)

    return templates.TemplateResponse(
        "quiz.html",
        {
            "request": request,
            "questions": questions,
        },
    )


@app.post("/submit-quiz")
async def submit_quiz(request: Request):
    user = get_current_user(request)
    if not user or user["role"] != "student":
        return RedirectResponse(url="/login", status_code=303)

    form = await request.form()
    skills = json.loads(user["skills"] or "{}")

    score = 0
    for i in range(10):
        topic = form.get(f"topic_{i}")
        correct_index = int(form.get(f"correct_{i}", 0))
        answer = int(form.get(f"answer_{i}", -1))
        is_correct = answer == correct_index

        if is_correct:
            score += 1

        if topic in skills:
            skills[topic] = update_skill_score(skills[topic], is_correct)

    xp_earned = score * 10
    updated_xp = user["xp"] + xp_earned
    updated_level = calculate_level(updated_xp)

    update_user_progress(
        email=user["email"],
        skills_json=json.dumps(skills),
        xp=updated_xp,
        level=updated_level,
    )

    return templates.TemplateResponse(
        "quiz_result.html",
        {
            "request": request,
            "score": score,
            "xp_earned": xp_earned,
            "level": updated_level,
        },
    )
