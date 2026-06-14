from datetime import datetime
from uuid import UUID

from fastapi import APIRouter, Depends

from src.application.command_handlers.check_in_ticket_handler import (
    CheckInTicketCommandHandler,
)
from src.application.commands.check_in_ticket_command import CheckInTicketCommand
from src.application.queries.view_purchased_tickets_query import (
    ViewPurchasedTicketsQuery,
)
from src.application.query_handlers.view_purchased_tickets_handler import (
    ViewPurchasedTicketsQueryHandler,
)
from src.presentation.api.error_mapper import to_http_error
from src.presentation.dependencies import (
    get_check_in_ticket_handler,
    get_view_purchased_tickets_handler,
)
from src.presentation.schemas.ticket_schemas import (
    CheckInTicketRequest,
    CheckInTicketResponse,
    PurchasedTicketResponse,
)

router = APIRouter(
    tags=["Tickets"],
)


@router.get(
    "/customers/{customer_id}/tickets",
    response_model=list[PurchasedTicketResponse],
)
def view_purchased_tickets(
    customer_id: UUID,
    handler: ViewPurchasedTicketsQueryHandler = Depends(
        get_view_purchased_tickets_handler
    ),
):
    try:
        results = handler.handle(
            ViewPurchasedTicketsQuery(
                customer_id=customer_id,
            )
        )

        return [
            PurchasedTicketResponse(
                ticket_id=ticket.ticket_id,
                booking_id=ticket.booking_id,
                event_id=ticket.event_id,
                event_name=ticket.event_name,
                ticket_category_id=ticket.ticket_category_id,
                ticket_category_name=ticket.ticket_category_name,
                ticket_code=ticket.ticket_code,
                status=ticket.status,
                checked_in_at=ticket.checked_in_at,
            )
            for ticket in results
        ]

    except Exception as error:
        raise to_http_error(error)


@router.post(
    "/tickets/check-in",
    response_model=CheckInTicketResponse,
)
def check_in_ticket(
    request: CheckInTicketRequest,
    handler: CheckInTicketCommandHandler = Depends(get_check_in_ticket_handler),
):
    try:
        checked_in_at = request.checked_in_at or datetime.now()

        result = handler.handle(
            CheckInTicketCommand(
                event_id=request.event_id,
                ticket_code=request.ticket_code,
                checked_in_at=checked_in_at,
            )
        )

        return CheckInTicketResponse(
            ticket_code=result.ticket_code,
            event_id=result.event_id,
            booking_id=result.booking_id,
            status=result.status,
            checked_in_at=result.checked_in_at,
        )

    except Exception as error:
        raise to_http_error(error)