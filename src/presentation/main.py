from fastapi import FastAPI

from src.infrastructure.database import create_tables
from src.presentation.api import event_router, ticket_category_router

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


app.include_router(event_router)
app.include_router(ticket_category_router)