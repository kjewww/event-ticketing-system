from uuid import UUID

from fastapi import APIRouter, Depends

from src.application.command_handlers.create_ticket_category_handler import (
    CreateTicketCategoryCommandHandler,
)
from src.application.command_handlers.disable_ticket_category_handler import (
    DisableTicketCategoryCommandHandler,
)
from src.application.commands.create_ticket_category_command import (
    CreateTicketCategoryCommand,
)
from src.application.commands.disable_ticket_category_command import (
    DisableTicketCategoryCommand,
)
from src.presentation.api.error_mapper import to_http_error
from src.presentation.dependencies import (
    get_create_ticket_category_handler,
    get_disable_ticket_category_handler,
)
from src.presentation.schemas.ticket_category_schemas import (
    CreateTicketCategoryRequest,
    DisableTicketCategoryRequest,
    DisableTicketCategoryResponse,
    TicketCategoryResponse,
)

router = APIRouter(
    prefix="/events/{event_id}/ticket-categories",
    tags=["Ticket Categories"],
)


@router.post(
    "",
    response_model=TicketCategoryResponse,
    status_code=201,
)
def create_ticket_category(
    event_id: UUID,
    request: CreateTicketCategoryRequest,
    handler: CreateTicketCategoryCommandHandler = Depends(
        get_create_ticket_category_handler
    ),
):
    try:
        result = handler.handle(
            CreateTicketCategoryCommand(
                event_id=event_id,
                organizer_id=request.organizer_id,
                name=request.name,
                price_amount=request.price_amount,
                currency=request.currency,
                quota=request.quota,
                sales_start_date=request.sales_start_date,
                sales_end_date=request.sales_end_date,
            )
        )

        return TicketCategoryResponse(
            event_id=result.event_id,
            ticket_category_id=result.ticket_category_id,
            name=result.name,
            price_amount=result.price_amount,
            currency=result.currency,
            quota=result.quota,
            sales_start_date=result.sales_start_date,
            sales_end_date=result.sales_end_date,
            is_active=result.is_active,
        )

    except Exception as error:
        raise to_http_error(error)


@router.patch(
    "/{ticket_category_id}/disable",
    response_model=DisableTicketCategoryResponse,
)
def disable_ticket_category(
    event_id: UUID,
    ticket_category_id: UUID,
    request: DisableTicketCategoryRequest,
    handler: DisableTicketCategoryCommandHandler = Depends(
        get_disable_ticket_category_handler
    ),
):
    try:
        result = handler.handle(
            DisableTicketCategoryCommand(
                event_id=event_id,
                organizer_id=request.organizer_id,
                ticket_category_id=ticket_category_id,
            )
        )

        return DisableTicketCategoryResponse(
            event_id=result.event_id,
            ticket_category_id=result.ticket_category_id,
            name=result.name,
            is_active=result.is_active,
        )

    except Exception as error:
        raise to_http_error(error)