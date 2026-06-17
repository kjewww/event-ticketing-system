from datetime import datetime
from uuid import UUID

from fastapi import APIRouter, Depends

from src.application.command_handlers.create_booking_handler import (
    CreateBookingCommandHandler,
)
from src.application.command_handlers.expire_booking_handler import (
    ExpireBookingCommandHandler,
)
from src.application.command_handlers.pay_booking_handler import (
    PayBookingCommandHandler,
)
from src.application.commands.create_booking_command import CreateBookingCommand
from src.application.commands.expire_booking_command import ExpireBookingCommand
from src.application.commands.pay_booking_command import PayBookingCommand
from src.presentation.api.error_mapper import to_http_error
from src.presentation.dependencies import (
    get_create_booking_handler,
    get_expire_booking_handler,
    get_pay_booking_handler,
)
from src.presentation.schemas.booking_schemas import (
    CreateBookingRequest,
    CreateBookingResponse,
    ExpireBookingRequest,
    ExpireBookingResponse,
    PayBookingRequest,
    PayBookingResponse,
)

router = APIRouter(
    prefix="/bookings",
    tags=["Bookings"],
)


@router.post(
    "",
    response_model=CreateBookingResponse,
    status_code=201,
)
def create_booking(
    request: CreateBookingRequest,
    handler: CreateBookingCommandHandler = Depends(get_create_booking_handler),
):
    try:
        requested_at = request.requested_at or datetime.now()

        result = handler.handle(
            CreateBookingCommand(
                customer_id=request.customer_id,
                customer_name=request.customer_name,
                event_id=request.event_id,
                ticket_category_id=request.ticket_category_id,
                quantity=request.quantity,
                requested_at=requested_at,
                service_fee_amount=request.service_fee_amount,
                currency=request.currency,
            )
        )

        return CreateBookingResponse(
            booking_id=result.booking_id,
            customer_id=result.customer_id,
            event_id=result.event_id,
            ticket_category_id=result.ticket_category_id,
            quantity=result.quantity,
            total_price_amount=result.total_price_amount,
            currency=result.currency,
            payment_deadline_at=result.payment_deadline_at,
            status=result.status,
        )

    except Exception as error:
        raise to_http_error(error)


@router.post(
    "/{booking_id}/pay",
    response_model=PayBookingResponse,
)
def pay_booking(
    booking_id: UUID,
    request: PayBookingRequest,
    handler: PayBookingCommandHandler = Depends(get_pay_booking_handler),
):
    try:
        paid_at = request.paid_at or datetime.now()

        result = handler.handle(
            PayBookingCommand(
                booking_id=booking_id,
                customer_id=request.customer_id,
                amount=request.amount,
                paid_at=paid_at,
                currency=request.currency,
            )
        )

        return PayBookingResponse(
            booking_id=result.booking_id,
            status=result.status,
            total_price_amount=result.total_price_amount,
            currency=result.currency,
            ticket_codes=result.ticket_codes,
            payment_reference=result.payment_reference,
        )

    except Exception as error:
        raise to_http_error(error)


@router.post(
    "/{booking_id}/expire",
    response_model=ExpireBookingResponse,
)
def expire_booking(
    booking_id: UUID,
    request: ExpireBookingRequest,
    handler: ExpireBookingCommandHandler = Depends(get_expire_booking_handler),
):
    try:
        now = request.now or datetime.now()

        result = handler.handle(
            ExpireBookingCommand(
                booking_id=booking_id,
                now=now,
            )
        )

        return ExpireBookingResponse(
            booking_id=result.booking_id,
            status=result.status,
        )

    except Exception as error:
        raise to_http_error(error)