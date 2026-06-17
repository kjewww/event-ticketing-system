from src.application.commands.request_refund_command import RequestRefundCommand
from src.application.dto.refund_dto import RequestRefundResponseDTO
from src.application.interfaces.unit_of_work import UnitOfWork

from src.domain.aggregates.refund import Refund
from src.domain.repositories.booking_repository import BookingRepository
from src.domain.repositories.event_repository import EventRepository
from src.domain.repositories.refund_repository import RefundRepository
from src.domain.services.refund_policy import RefundPolicy


class RequestRefundCommandHandler:
    def __init__(
        self,
        booking_repository: BookingRepository,
        event_repository: EventRepository,
        refund_repository: RefundRepository,
        unit_of_work: UnitOfWork,
        refund_policy: RefundPolicy | None = None,
    ):
        self.booking_repository = booking_repository
        self.event_repository = event_repository
        self.refund_repository = refund_repository
        self.unit_of_work = unit_of_work
        self.refund_policy = refund_policy or RefundPolicy()

    def handle(
        self,
        command: RequestRefundCommand,
    ) -> RequestRefundResponseDTO:
        try:
            booking = self.booking_repository.get_by_id(command.booking_id)

            if booking is None:
                raise ValueError("Booking not found.")

            if booking.customer_id != command.customer_id:
                raise PermissionError("Only the booking owner can request a refund.")

            event = self.event_repository.get_by_id(booking.event_id)

            if event is None:
                raise ValueError("Event not found.")

            existing_refund = self.refund_repository.get_by_booking_id(booking.id)

            if existing_refund is not None:
                raise ValueError("Refund request already exists for this booking.")

            self.refund_policy.ensure_refund_allowed(
                booking=booking,
                event_status=event.status,
                refund_deadline=command.refund_deadline,
                requested_at=command.requested_at,
            )

            refund = Refund.request(
                booking_id=booking.id,
                customer_id=booking.customer_id,
                amount=booking.total_price,
                reason=command.reason,
            )

            self.refund_repository.save(refund)
            self.unit_of_work.commit()

            return RequestRefundResponseDTO(
                refund_id=refund.id,
                booking_id=refund.booking_id,
                customer_id=refund.customer_id,
                amount=refund.amount.amount,
                currency=refund.amount.currency,
                status=refund.status.value,
                reason=refund.reason,
            )

        except Exception:
            self.unit_of_work.rollback()
            raise