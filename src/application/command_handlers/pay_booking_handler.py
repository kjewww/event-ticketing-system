from decimal import Decimal

from src.application.commands.pay_booking_command import PayBookingCommand
from src.application.dto.booking_dto import PayBookingResponseDTO
from src.application.interfaces.payment_gateway import PaymentGateway
from src.application.interfaces.ticket_code_generator import TicketCodeGenerator
from src.application.interfaces.unit_of_work import UnitOfWork

from src.domain.repositories.booking_repository import BookingRepository
from src.domain.value_objects.money import Money


class PayBookingCommandHandler:
    def __init__(
        self,
        booking_repository: BookingRepository,
        payment_gateway: PaymentGateway,
        ticket_code_generator: TicketCodeGenerator,
        unit_of_work: UnitOfWork,
    ):
        self.booking_repository = booking_repository
        self.payment_gateway = payment_gateway
        self.ticket_code_generator = ticket_code_generator
        self.unit_of_work = unit_of_work

    def handle(
        self,
        command: PayBookingCommand,
    ) -> PayBookingResponseDTO:
        try:
            booking = self.booking_repository.get_by_id(command.booking_id)

            if booking is None:
                raise ValueError("Booking not found.")

            if booking.customer_id != command.customer_id:
                raise PermissionError("Only the booking owner can pay this booking.")

            amount = Money(
                amount=Decimal(str(command.amount)),
                currency=command.currency,
            )

            ticket_codes = self.ticket_code_generator.generate_many(
                booking.quantity
            )

            booking.pay(
                amount=amount,
                paid_at=command.paid_at,
                ticket_codes=ticket_codes,
            )

            payment_reference = self.payment_gateway.process_payment(
                booking_id=booking.id,
                customer_id=booking.customer_id,
                amount=amount,
            )

            self.booking_repository.save(booking)
            self.unit_of_work.commit()

            return PayBookingResponseDTO(
                booking_id=booking.id,
                status=booking.status.value,
                total_price_amount=booking.total_price.amount,
                currency=booking.total_price.currency,
                ticket_codes=[
                    ticket.ticket_code.value
                    for ticket in booking.tickets
                ],
                payment_reference=payment_reference,
            )

        except Exception:
            self.unit_of_work.rollback()
            raise