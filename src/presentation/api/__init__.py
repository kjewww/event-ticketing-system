from src.presentation.api.booking_routes import router as booking_router
from src.presentation.api.event_routes import router as event_router
from src.presentation.api.refund_routes import router as refund_router
from src.presentation.api.report_routes import router as report_router
from src.presentation.api.ticket_category_routes import (
    router as ticket_category_router,
)
from src.presentation.api.ticket_routes import router as ticket_router

__all__ = [
    "event_router",
    "ticket_category_router",
    "booking_router",
    "ticket_router",
    "refund_router",
    "report_router",
]