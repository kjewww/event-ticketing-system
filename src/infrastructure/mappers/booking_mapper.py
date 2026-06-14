from src.domain.aggregates.booking import Booking
from src.domain.value_objects.booking_status import BookingStatus
from src.domain.value_objects.money import Money
from src.domain.value_objects.payment_deadline import PaymentDeadline

from src.infrastructure.database.models.booking_model import BookingModel
from src.infrastructure.mappers.ticket_mapper import TicketMapper


class BookingMapper:
    @staticmethod
    def to_domain(model: BookingModel) -> Booking:
        tickets = [
            TicketMapper.to_domain(ticket_model)
            for ticket_model in model.tickets
        ]

        return Booking.reconstruct(
            id=model.id,
            customer_id=model.customer_id,
            customer_name=model.customer_name,
            event_id=model.event_id,
            ticket_category_id=model.ticket_category_id,
            quantity=model.quantity,
            unit_price=Money(
                amount=model.unit_price_amount,
                currency=model.unit_price_currency,
            ),
            payment_deadline=PaymentDeadline(model.payment_deadline_at),
            service_fee=Money(
                amount=model.service_fee_amount,
                currency=model.service_fee_currency,
            ),
            status=BookingStatus(model.status),
            refund_required=model.refund_required,
            tickets=tickets,
        )

    @staticmethod
    def to_model(domain: Booking) -> BookingModel:
        model = BookingModel(
            id=domain.id,
            customer_id=domain.customer_id,
            customer_name=domain.customer_name,
            event_id=domain.event_id,
            ticket_category_id=domain.ticket_category_id,
            quantity=domain.quantity,
            unit_price_amount=domain.unit_price.amount,
            unit_price_currency=domain.unit_price.currency,
            service_fee_amount=domain.service_fee.amount,
            service_fee_currency=domain.service_fee.currency,
            total_price_amount=domain.total_price.amount,
            total_price_currency=domain.total_price.currency,
            payment_deadline_at=domain.payment_deadline.deadline_at,
            status=domain.status.value,
            refund_required=domain.refund_required,
        )

        model.tickets = [
            TicketMapper.to_model(ticket)
            for ticket in domain.tickets
        ]

        return model