from src.application.commands.reject_refund_command import RejectRefundCommand
from src.application.dto.refund_dto import RejectRefundResponseDTO
from src.application.interfaces.unit_of_work import UnitOfWork

from src.domain.repositories.booking_repository import BookingRepository
from src.domain.repositories.event_repository import EventRepository
from src.domain.repositories.refund_repository import RefundRepository


class RejectRefundCommandHandler:
    def __init__(
        self,
        refund_repository: RefundRepository,
        booking_repository: BookingRepository,
        event_repository: EventRepository,
        unit_of_work: UnitOfWork,
    ):
        self.refund_repository = refund_repository
        self.booking_repository = booking_repository
        self.event_repository = event_repository
        self.unit_of_work = unit_of_work

    def handle(
        self,
        command: RejectRefundCommand,
    ) -> RejectRefundResponseDTO:
        try:
            refund = self.refund_repository.get_by_id(command.refund_id)

            if refund is None:
                raise ValueError("Refund not found.")

            booking = self.booking_repository.get_by_id(refund.booking_id)

            if booking is None:
                raise ValueError("Booking not found.")

            event = self.event_repository.get_by_id(booking.event_id)

            if event is None:
                raise ValueError("Event not found.")

            if event.organizer_id != command.organizer_id:
                raise PermissionError("Only the event organizer can reject this refund.")

            refund.reject(command.rejection_reason)

            self.refund_repository.save(refund)
            self.unit_of_work.commit()

            return RejectRefundResponseDTO(
                refund_id=refund.id,
                booking_id=refund.booking_id,
                status=refund.status.value,
                rejection_reason=refund.rejection_reason,
            )

        except Exception:
            self.unit_of_work.rollback()
            raise