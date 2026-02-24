from fastapi import FastAPI
from fastapi.responses import RedirectResponse

from app import database
from app.auth import router as auth_router

app = FastAPI()
app.include_router(auth_router)


@app.on_event("startup")
def startup_event() -> None:
    database.create_tables()


@app.get("/")
def read_root() -> RedirectResponse:
    return RedirectResponse(url="/login", status_code=303)
