from contextlib import asynccontextmanager

from fastapi import FastAPI

from src.infrastructure.database import create_tables
from src.presentation.api import (
    booking_router,
    event_router,
    ticket_category_router,
    ticket_router,
)


@asynccontextmanager
async def lifespan(app: FastAPI):
    create_tables()
    yield


app = FastAPI(
    title="Event Ticketing System API",
    version="1.0.0",
    lifespan=lifespan,
)


@app.get("/")
def root():
    return {
        "message": "Event Ticketing System API",
        "status": "running",
    }


app.include_router(event_router)
app.include_router(ticket_category_router)
app.include_router(booking_router)
app.include_router(ticket_router)