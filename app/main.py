from fastapi import FastAPI
from fastapi.responses import HTMLResponse

from app import database

app = FastAPI()


@app.on_event("startup")
def startup_event() -> None:
    database.create_tables()


@app.get("/", response_class=HTMLResponse)
def read_root() -> str:
    return "<h1>Grammar AI Platform is Running</h1>"
