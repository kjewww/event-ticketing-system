from fastapi import FastAPI

from src.infrastructure.database import create_tables

app = FastAPI(
    title="Event Ticketing System API",
    version="1.0.0",
)


@app.on_event("startup")
def startup() -> None:
    create_tables()


@app.get("/")
def root():
    return {
        "message": "Event Ticketing System API",
        "status": "running",
    }