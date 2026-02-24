import hashlib
import hmac
import json
from urllib.parse import quote, unquote

from fastapi import APIRouter, Form, Request
from fastapi.responses import RedirectResponse
from fastapi.templating import Jinja2Templates

from app.models import create_user, get_all_students, get_user_by_email

router = APIRouter()
templates: Jinja2Templates | None = None

SESSION_COOKIE_NAME = "session"
SESSION_SECRET = "dev-secret-key"


def configure_templates(template_engine: Jinja2Templates) -> None:
    global templates
    templates = template_engine


def create_signed_session_value(email: str) -> str:
    signature = hmac.new(
        SESSION_SECRET.encode("utf-8"),
        email.encode("utf-8"),
        hashlib.sha256,
    ).hexdigest()
    return f"{quote(email)}|{signature}"


def verify_signed_session_value(cookie_value: str | None) -> str | None:
    if not cookie_value or "|" not in cookie_value:
        return None

    encoded_email, signature = cookie_value.split("|", 1)
    email = unquote(encoded_email)
    expected_signature = hmac.new(
        SESSION_SECRET.encode("utf-8"),
        email.encode("utf-8"),
        hashlib.sha256,
    ).hexdigest()

    if not hmac.compare_digest(signature, expected_signature):
        return None

    return email


def get_current_user(request: Request):
    cookie_value = request.cookies.get(SESSION_COOKIE_NAME)
    email = verify_signed_session_value(cookie_value)
    if not email:
        return None
    return get_user_by_email(email)


@router.get("/login")
def login_page(request: Request):
    return templates.TemplateResponse(
        "login.html",
        {
            "request": request,
            "error": None,
            "show_create_user": False,
            "created_message": None,
        },
    )


@router.post("/login")
def login_submit(request: Request, email: str = Form(...), password: str = Form(...)):
    user = get_user_by_email(email)

    if not user or user["password"] != password:
        return templates.TemplateResponse(
            "login.html",
            {
                "request": request,
                "error": "Invalid email or password.",
                "show_create_user": False,
                "created_message": None,
            },
        )

    if user["role"] == "student":
        redirect_target = "/student"
    else:
        redirect_target = "/teacher"

    response = RedirectResponse(url=redirect_target, status_code=303)
    response.set_cookie(
        key=SESSION_COOKIE_NAME,
        value=create_signed_session_value(user["email"]),
        httponly=True,
    )
    return response


@router.get("/logout")
def logout():
    response = RedirectResponse(url="/login", status_code=303)
    response.delete_cookie(SESSION_COOKIE_NAME)
    return response


@router.get("/student")
def student_dashboard(request: Request):
    user = get_current_user(request)
    if not user or user["role"] != "student":
        return RedirectResponse(url="/login", status_code=303)

    skills = {}
    if user["skills"]:
        skills = json.loads(user["skills"])

    return templates.TemplateResponse(
        "student_dashboard.html",
        {
            "request": request,
            "email": user["email"],
            "xp": user["xp"],
            "level": user["level"],
            "skills": skills,
        },
    )


@router.get("/teacher")
def teacher_dashboard(request: Request):
    user = get_current_user(request)
    if not user or user["role"] != "teacher":
        return RedirectResponse(url="/login", status_code=303)

    students = get_all_students()

    return templates.TemplateResponse(
        "teacher_dashboard.html",
        {
            "request": request,
            "email": user["email"],
            "students": students,
        },
    )


@router.get("/create-user")
def create_user_page(request: Request):
    return templates.TemplateResponse(
        "login.html",
        {
            "request": request,
            "error": None,
            "show_create_user": True,
            "created_message": None,
        },
    )


@router.post("/create-user")
def create_user_submit(
    request: Request,
    email: str = Form(...),
    password: str = Form(...),
    role: str = Form(...),
    grade: int | None = Form(default=None),
):
    try:
        create_user(email=email, password=password, role=role, grade=grade)
        message = "User created successfully."
    except Exception:
        message = "Could not create user. Email may already exist."

    return templates.TemplateResponse(
        "login.html",
        {
            "request": request,
            "error": None,
            "show_create_user": True,
            "created_message": message,
        },
    )
