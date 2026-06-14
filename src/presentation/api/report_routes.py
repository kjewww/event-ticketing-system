from uuid import UUID

from fastapi import APIRouter, Depends, Query

from src.application.queries.view_event_participants_query import (
    ViewEventParticipantsQuery,
)
from src.application.queries.view_event_sales_report_query import (
    ViewEventSalesReportQuery,
)
from src.application.query_handlers.view_event_participants_handler import (
    ViewEventParticipantsQueryHandler,
)
from src.application.query_handlers.view_event_sales_report_handler import (
    ViewEventSalesReportQueryHandler,
)
from src.presentation.api.error_mapper import to_http_error
from src.presentation.dependencies import (
    get_view_event_participants_handler,
    get_view_event_sales_report_handler,
)
from src.presentation.schemas.report_schemas import (
    BookingStatusCountResponse,
    EventParticipantResponse,
    EventSalesReportResponse,
    TicketCategorySalesResponse,
)

router = APIRouter(
    prefix="/events/{event_id}",
    tags=["Reports"],
)


@router.get(
    "/sales-report",
    response_model=EventSalesReportResponse,
)
def view_event_sales_report(
    event_id: UUID,
    organizer_id: UUID = Query(...),
    handler: ViewEventSalesReportQueryHandler = Depends(
        get_view_event_sales_report_handler
    ),
):
    try:
        result = handler.handle(
            ViewEventSalesReportQuery(
                event_id=event_id,
                organizer_id=organizer_id,
            )
        )

        return EventSalesReportResponse(
            event_id=result.event_id,
            tickets_sold_per_category=[
                TicketCategorySalesResponse(
                    ticket_category_id=item.ticket_category_id,
                    ticket_category_name=item.ticket_category_name,
                    tickets_sold=item.tickets_sold,
                )
                for item in result.tickets_sold_per_category
            ],
            booking_status_counts=[
                BookingStatusCountResponse(
                    status=item.status,
                    count=item.count,
                )
                for item in result.booking_status_counts
            ],
            total_revenue_amount=result.total_revenue_amount,
            currency=result.currency,
        )

    except Exception as error:
        raise to_http_error(error)


@router.get(
    "/participants",
    response_model=list[EventParticipantResponse],
)
def view_event_participants(
    event_id: UUID,
    organizer_id: UUID = Query(...),
    handler: ViewEventParticipantsQueryHandler = Depends(
        get_view_event_participants_handler
    ),
):
    try:
        results = handler.handle(
            ViewEventParticipantsQuery(
                event_id=event_id,
                organizer_id=organizer_id,
            )
        )

        return [
            EventParticipantResponse(
                customer_id=participant.customer_id,
                customer_name=participant.customer_name,
                ticket_category_name=participant.ticket_category_name,
                ticket_code=participant.ticket_code,
                check_in_status=participant.check_in_status,
            )
            for participant in results
        ]

    except Exception as error:
        raise to_http_error(error)