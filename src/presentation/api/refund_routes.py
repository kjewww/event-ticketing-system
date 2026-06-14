from datetime import datetime
from uuid import UUID

from fastapi import APIRouter, Depends

from src.application.command_handlers.approve_refund_handler import (
    ApproveRefundCommandHandler,
)
from src.application.command_handlers.mark_refund_paid_out_handler import (
    MarkRefundPaidOutCommandHandler,
)
from src.application.command_handlers.reject_refund_handler import (
    RejectRefundCommandHandler,
)
from src.application.command_handlers.request_refund_handler import (
    RequestRefundCommandHandler,
)
from src.application.commands.approve_refund_command import ApproveRefundCommand
from src.application.commands.mark_refund_paid_out_command import (
    MarkRefundPaidOutCommand,
)
from src.application.commands.reject_refund_command import RejectRefundCommand
from src.application.commands.request_refund_command import RequestRefundCommand
from src.presentation.api.error_mapper import to_http_error
from src.presentation.dependencies import (
    get_approve_refund_handler,
    get_mark_refund_paid_out_handler,
    get_reject_refund_handler,
    get_request_refund_handler,
)
from src.presentation.schemas.refund_schemas import (
    ApproveRefundRequest,
    ApproveRefundResponse,
    MarkRefundPaidOutRequest,
    MarkRefundPaidOutResponse,
    RejectRefundRequest,
    RejectRefundResponse,
    RequestRefundRequest,
    RequestRefundResponse,
)

router = APIRouter(
    tags=["Refunds"],
)


@router.post(
    "/bookings/{booking_id}/refunds",
    response_model=RequestRefundResponse,
    status_code=201,
)
def request_refund(
    booking_id: UUID,
    request: RequestRefundRequest,
    handler: RequestRefundCommandHandler = Depends(get_request_refund_handler),
):
    try:
        requested_at = request.requested_at or datetime.now()

        result = handler.handle(
            RequestRefundCommand(
                booking_id=booking_id,
                customer_id=request.customer_id,
                reason=request.reason,
                requested_at=requested_at,
                refund_deadline=request.refund_deadline,
            )
        )

        return RequestRefundResponse(
            refund_id=result.refund_id,
            booking_id=result.booking_id,
            customer_id=result.customer_id,
            amount=result.amount,
            currency=result.currency,
            status=result.status,
            reason=result.reason,
        )

    except Exception as error:
        raise to_http_error(error)


@router.post(
    "/refunds/{refund_id}/approve",
    response_model=ApproveRefundResponse,
)
def approve_refund(
    refund_id: UUID,
    request: ApproveRefundRequest,
    handler: ApproveRefundCommandHandler = Depends(get_approve_refund_handler),
):
    try:
        result = handler.handle(
            ApproveRefundCommand(
                refund_id=refund_id,
                organizer_id=request.organizer_id,
            )
        )

        return ApproveRefundResponse(
            refund_id=result.refund_id,
            booking_id=result.booking_id,
            status=result.status,
        )

    except Exception as error:
        raise to_http_error(error)


@router.post(
    "/refunds/{refund_id}/reject",
    response_model=RejectRefundResponse,
)
def reject_refund(
    refund_id: UUID,
    request: RejectRefundRequest,
    handler: RejectRefundCommandHandler = Depends(get_reject_refund_handler),
):
    try:
        result = handler.handle(
            RejectRefundCommand(
                refund_id=refund_id,
                organizer_id=request.organizer_id,
                rejection_reason=request.rejection_reason,
            )
        )

        return RejectRefundResponse(
            refund_id=result.refund_id,
            booking_id=result.booking_id,
            status=result.status,
            rejection_reason=result.rejection_reason,
        )

    except Exception as error:
        raise to_http_error(error)


@router.post(
    "/refunds/{refund_id}/paid-out",
    response_model=MarkRefundPaidOutResponse,
)
def mark_refund_paid_out(
    refund_id: UUID,
    request: MarkRefundPaidOutRequest,
    handler: MarkRefundPaidOutCommandHandler = Depends(
        get_mark_refund_paid_out_handler
    ),
):
    try:
        result = handler.handle(
            MarkRefundPaidOutCommand(
                refund_id=refund_id,
                admin_id=request.admin_id,
            )
        )

        return MarkRefundPaidOutResponse(
            refund_id=result.refund_id,
            booking_id=result.booking_id,
            status=result.status,
            payment_reference=result.payment_reference,
        )

    except Exception as error:
        raise to_http_error(error)