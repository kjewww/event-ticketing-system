from datetime import date
from uuid import UUID

from fastapi import APIRouter, Depends, Query

from src.application.command_handlers.cancel_event_handler import (
    CancelEventCommandHandler,
)
from src.application.command_handlers.create_event_handler import (
    CreateEventCommandHandler,
)
from src.application.command_handlers.publish_event_handler import (
    PublishEventCommandHandler,
)
from src.application.commands.cancel_event_command import CancelEventCommand
from src.application.commands.create_event_command import CreateEventCommand
from src.application.commands.publish_event_command import PublishEventCommand
from src.application.queries.view_available_events_query import (
    ViewAvailableEventsQuery,
)
from src.application.queries.view_event_details_query import ViewEventDetailsQuery
from src.application.query_handlers.view_available_events_handler import (
    ViewAvailableEventsQueryHandler,
)
from src.application.query_handlers.view_event_details_handler import (
    ViewEventDetailsQueryHandler,
)
from src.presentation.api.error_mapper import to_http_error
from src.presentation.dependencies import (
    get_cancel_event_handler,
    get_create_event_handler,
    get_publish_event_handler,
    get_view_available_events_handler,
    get_view_event_details_handler,
)
from src.presentation.schemas.event_schemas import (
    AvailableEventResponse,
    CreateEventRequest,
    EventDetailsResponse,
    EventResponse,
    EventStatusResponse,
    EventTicketCategoryResponse,
    OrganizerActionRequest,
)

router = APIRouter(
    prefix="/events",
    tags=["Events"],
)


@router.post(
    "",
    response_model=EventResponse,
    status_code=201,
)
def create_event(
    request: CreateEventRequest,
    handler: CreateEventCommandHandler = Depends(get_create_event_handler),
):
    try:
        result = handler.handle(
            CreateEventCommand(
                organizer_id=request.organizer_id,
                name=request.name,
                description=request.description,
                start_date=request.start_date,
                end_date=request.end_date,
                location=request.location,
                capacity=request.capacity,
            )
        )

        return EventResponse(
            event_id=result.event_id,
            organizer_id=result.organizer_id,
            name=result.name,
            description=result.description,
            start_date=result.start_date,
            end_date=result.end_date,
            location=result.location,
            capacity=result.capacity,
            status=result.status,
        )

    except Exception as error:
        raise to_http_error(error)


@router.get(
    "/available",
    response_model=list[AvailableEventResponse],
)
def view_available_events(
    date_filter: date | None = Query(default=None),
    location: str | None = Query(default=None),
    handler: ViewAvailableEventsQueryHandler = Depends(
        get_view_available_events_handler
    ),
):
    try:
        results = handler.handle(
            ViewAvailableEventsQuery(
                date_filter=date_filter,
                location=location,
            )
        )

        return [
            AvailableEventResponse(
                event_id=event.event_id,
                name=event.name,
                start_date=event.start_date,
                end_date=event.end_date,
                location=event.location,
                lowest_ticket_price=event.lowest_ticket_price,
            )
            for event in results
        ]

    except Exception as error:
        raise to_http_error(error)


@router.get(
    "/{event_id}",
    response_model=EventDetailsResponse,
)
def view_event_details(
    event_id: UUID,
    handler: ViewEventDetailsQueryHandler = Depends(
        get_view_event_details_handler
    ),
):
    try:
        result = handler.handle(
            ViewEventDetailsQuery(event_id=event_id)
        )

        return EventDetailsResponse(
            event_id=result.event_id,
            name=result.name,
            description=result.description,
            start_date=result.start_date,
            end_date=result.end_date,
            location=result.location,
            organizer_id=result.organizer_id,
            status=result.status,
            ticket_categories=[
                EventTicketCategoryResponse(
                    ticket_category_id=category.ticket_category_id,
                    name=category.name,
                    price_amount=category.price_amount,
                    currency=category.currency,
                    quota=category.quota,
                    remaining_quota=category.remaining_quota,
                    sales_start_date=category.sales_start_date,
                    sales_end_date=category.sales_end_date,
                    is_active=category.is_active,
                    purchase_status=category.purchase_status,
                )
                for category in result.ticket_categories
            ],
        )

    except Exception as error:
        raise to_http_error(error)


@router.post(
    "/{event_id}/publish",
    response_model=EventStatusResponse,
)
def publish_event(
    event_id: UUID,
    request: OrganizerActionRequest,
    handler: PublishEventCommandHandler = Depends(get_publish_event_handler),
):
    try:
        result = handler.handle(
            PublishEventCommand(
                event_id=event_id,
                organizer_id=request.organizer_id,
            )
        )

        return EventStatusResponse(
            event_id=result.event_id,
            name=result.name,
            status=result.status,
        )

    except Exception as error:
        raise to_http_error(error)


@router.post(
    "/{event_id}/cancel",
    response_model=EventStatusResponse,
)
def cancel_event(
    event_id: UUID,
    request: OrganizerActionRequest,
    handler: CancelEventCommandHandler = Depends(get_cancel_event_handler),
):
    try:
        result = handler.handle(
            CancelEventCommand(
                event_id=event_id,
                organizer_id=request.organizer_id,
            )
        )

        return EventStatusResponse(
            event_id=result.event_id,
            name=result.name,
            status=result.status,
        )

    except Exception as error:
        raise to_http_error(error)