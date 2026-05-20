from src.application.commands.cancel_event_command import CancelEventCommand
from src.application.dto.event_dto import CancelEventResponseDTO
from src.application.interfaces.unit_of_work import UnitOfWork

from src.domain.repositories.event_repository import EventRepository
from src.domain.repositories.booking_repository import BookingRepository
from src.domain.services.event_cancellation_service import EventCancellationService


class CancelEventCommandHandler:
    def __init__(
        self,
        event_repository: EventRepository,
        booking_repository: BookingRepository,
        unit_of_work: UnitOfWork,
        event_cancellation_service: EventCancellationService,
    ):
        self.event_repository = event_repository
        self.booking_repository = booking_repository
        self.unit_of_work = unit_of_work
        self.event_cancellation_service = event_cancellation_service

    def handle(self, command: CancelEventCommand) -> CancelEventResponseDTO:
        try:
            event = self.event_repository.get_by_id(command.event_id)

            if event is None:
                raise ValueError("Event not found.")

            if event.organizer_id != command.organizer_id:
                raise PermissionError(
                    "Only the event organizer can cancel this event."
                )

            paid_bookings = self.booking_repository.get_paid_bookings_by_event_id(
                event_id=event.id
            )

            self.event_cancellation_service.cancel_event_and_mark_paid_bookings(
                event=event,
                paid_bookings=paid_bookings,
            )

            self.event_repository.save(event)

            for booking in paid_bookings:
                self.booking_repository.save(booking)

            self.unit_of_work.commit()

            return CancelEventResponseDTO(
                event_id=event.id,
                name=event.name,
                status=event.status.value,
            )

        except Exception:
            self.unit_of_work.rollback()
            raise