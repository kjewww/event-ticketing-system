from src.presentation.api.booking_routes import router as booking_router
from src.presentation.api.event_routes import router as event_router
from src.presentation.api.ticket_category_routes import (
    router as ticket_category_router,
)

__all__ = [
    "event_router",
    "ticket_category_router",
    "booking_router",
]