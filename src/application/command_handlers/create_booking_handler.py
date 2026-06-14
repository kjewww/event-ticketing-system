from datetime import timedelta
from decimal import Decimal

from src.application.commands.create_booking_command import CreateBookingCommand
from src.application.dto.booking_dto import CreateBookingResponseDTO
from src.application.interfaces.unit_of_work import UnitOfWork

from src.domain.aggregates.booking import Booking
from src.domain.repositories.booking_repository import BookingRepository
from src.domain.repositories.event_repository import EventRepository
from src.domain.services.booking_policy import BookingPolicy
from src.domain.value_objects.money import Money
from src.domain.value_objects.payment_deadline import PaymentDeadline


class CreateBookingCommandHandler:
    def __init__(
        self,
        event_repository: EventRepository,
        booking_repository: BookingRepository,
        unit_of_work: UnitOfWork,
        booking_policy: BookingPolicy | None = None,
        payment_deadline_minutes: int = 15,
    ):
        self.event_repository = event_repository
        self.booking_repository = booking_repository
        self.unit_of_work = unit_of_work
        self.booking_policy = booking_policy or BookingPolicy()
        self.payment_deadline_minutes = payment_deadline_minutes

    def handle(
        self,
        command: CreateBookingCommand,
    ) -> CreateBookingResponseDTO:
        try:
            event = self.event_repository.get_by_id(command.event_id)

            if event is None:
                raise ValueError("Event not found.")

            ticket_category = event.get_ticket_category_by_id(
                command.ticket_category_id
            )

            if ticket_category is None:
                raise ValueError("Ticket category not found.")

            reserved_or_sold_quantity = (
                self.booking_repository.count_reserved_or_sold_quantity(
                    ticket_category.id
                )
            )
            remaining_quota = ticket_category.quota - reserved_or_sold_quantity

            has_active_booking = (
                self.booking_repository.has_active_booking_for_event(
                    customer_id=command.customer_id,
                    event_id=event.id,
                )
            )

            self.booking_policy.ensure_booking_allowed(
                event_status=event.status,
                ticket_category=ticket_category,
                quantity=command.quantity,
                remaining_quota=remaining_quota,
                has_active_booking_for_event=has_active_booking,
                requested_at=command.requested_at,
            )

            service_fee = Money(
                amount=Decimal(str(command.service_fee_amount)),
                currency=command.currency,
            )

            payment_deadline = PaymentDeadline(
                deadline_at=command.requested_at
                + timedelta(minutes=self.payment_deadline_minutes)
            )

            booking = Booking.create(
                customer_id=command.customer_id,
                customer_name=command.customer_name,
                event_id=event.id,
                ticket_category_id=ticket_category.id,
                quantity=command.quantity,
                unit_price=ticket_category.price,
                service_fee=service_fee,
                payment_deadline=payment_deadline,
            )

            self.booking_repository.save(booking)
            self.unit_of_work.commit()

            return CreateBookingResponseDTO(
                booking_id=booking.id,
                customer_id=booking.customer_id,
                event_id=booking.event_id,
                ticket_category_id=booking.ticket_category_id,
                quantity=booking.quantity,
                total_price_amount=booking.total_price.amount,
                currency=booking.total_price.currency,
                payment_deadline_at=booking.payment_deadline.deadline_at,
                status=booking.status.value,
            )

        except Exception:
            self.unit_of_work.rollback()
            raise