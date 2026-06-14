from src.application.commands.expire_booking_command import ExpireBookingCommand
from src.application.dto.booking_dto import ExpireBookingResponseDTO
from src.application.interfaces.unit_of_work import UnitOfWork

from src.domain.repositories.booking_repository import BookingRepository


class ExpireBookingCommandHandler:
    def __init__(
        self,
        booking_repository: BookingRepository,
        unit_of_work: UnitOfWork,
    ):
        self.booking_repository = booking_repository
        self.unit_of_work = unit_of_work

    def handle(
        self,
        command: ExpireBookingCommand,
    ) -> ExpireBookingResponseDTO:
        try:
            booking = self.booking_repository.get_by_id(command.booking_id)

            if booking is None:
                raise ValueError("Booking not found.")

            booking.expire(command.now)

            self.booking_repository.save(booking)
            self.unit_of_work.commit()

            return ExpireBookingResponseDTO(
                booking_id=booking.id,
                status=booking.status.value,
            )

        except Exception:
            self.unit_of_work.rollback()
            raise