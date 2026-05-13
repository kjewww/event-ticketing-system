from datetime import datetime
from decimal import Decimal
from uuid import UUID, uuid4

from src.domain.entities.ticket import Ticket
from src.domain.events.booking_events import BookingExpired, BookingPaid, TicketReserved
from src.domain.events.ticket_events import TicketCheckedIn
from src.domain.exceptions.domain_exception import (
    BookingCannotBePaidError,
    BookingCannotExpireError,
    BookingPaymentDeadlinePassedError,
    IncorrectPaymentAmountError,
    InvalidTicketQuantityError,
    TicketCannotBeCheckedInError,
)
from src.domain.value_objects.booking_status import BookingStatus
from src.domain.value_objects.money import Money
from src.domain.value_objects.payment_deadline import PaymentDeadline
from src.domain.value_objects.ticket_code import TicketCode
from src.domain.value_objects.ticket_status import TicketStatus


class Booking:
    def __init__(
        self,
        id: UUID,
        customer_id: UUID,
        event_id: UUID,
        ticket_category_id: UUID,
        quantity: int,
        unit_price: Money,
        payment_deadline: PaymentDeadline,
        service_fee: Money | None = None,
        status: BookingStatus = BookingStatus.PENDING_PAYMENT,
        refund_required: bool = False,
        tickets: list[Ticket] | None = None,
    ):
        if quantity <= 0:
            raise InvalidTicketQuantityError("Ticket quantity must be greater than zero.")

        self.id = id
        self.customer_id = customer_id
        self.event_id = event_id
        self.ticket_category_id = ticket_category_id
        self.quantity = quantity
        self.unit_price = unit_price
        self.service_fee = service_fee or Money(Decimal("0"), unit_price.currency)
        self.total_price = self.calculate_total_price()
        self.payment_deadline = payment_deadline
        self.status = status
        self.refund_required = refund_required
        self.tickets = tickets or []
        self._domain_events = []

    @classmethod
    def create(
        cls,
        customer_id: UUID,
        event_id: UUID,
        ticket_category_id: UUID,
        quantity: int,
        unit_price: Money,
        payment_deadline: PaymentDeadline,
        service_fee: Money | None = None,
    ) -> "Booking":
        booking = cls(
            id=uuid4(),
            customer_id=customer_id,
            event_id=event_id,
            ticket_category_id=ticket_category_id,
            quantity=quantity,
            unit_price=unit_price,
            payment_deadline=payment_deadline,
            service_fee=service_fee,
        )

        booking._domain_events.append(
            TicketReserved(
                booking_id=booking.id,
                customer_id=booking.customer_id,
                event_id=booking.event_id,
                ticket_category_id=booking.ticket_category_id,
                quantity=booking.quantity,
                total_price=booking.total_price,
            )
        )

        return booking

    def calculate_total_price(self) -> Money:
        ticket_total = self.unit_price.multiply(self.quantity)
        return ticket_total.add(self.service_fee)

    def pay(
        self,
        amount: Money,
        paid_at: datetime,
        ticket_codes: list[TicketCode],
    ) -> None:
        if self.status != BookingStatus.PENDING_PAYMENT:
            raise BookingCannotBePaidError("Only pending bookings can be paid.")

        if self.payment_deadline.has_passed(paid_at):
            raise BookingPaymentDeadlinePassedError("Payment deadline has passed.")

        if amount != self.total_price:
            raise IncorrectPaymentAmountError("Payment amount does not match total price.")

        if len(ticket_codes) != self.quantity:
            raise InvalidTicketQuantityError(
                "Number of ticket codes must match booking quantity."
            )

        if len(set(code.value for code in ticket_codes)) != len(ticket_codes):
            raise InvalidTicketQuantityError("Ticket codes must be unique.")

        self.status = BookingStatus.PAID

        for ticket_code in ticket_codes:
            ticket = Ticket(
                id=uuid4(),
                booking_id=self.id,
                event_id=self.event_id,
                ticket_category_id=self.ticket_category_id,
                ticket_code=ticket_code,
                status=TicketStatus.ACTIVE,
            )
            self.tickets.append(ticket)

        self._domain_events.append(
            BookingPaid(
                booking_id=self.id,
                customer_id=self.customer_id,
                event_id=self.event_id,
                total_price=self.total_price,
            )
        )

    def expire(self, now: datetime) -> None:
        if self.status == BookingStatus.PAID:
            raise BookingCannotExpireError("Paid booking cannot expire.")

        if self.status != BookingStatus.PENDING_PAYMENT:
            raise BookingCannotExpireError("Only pending bookings can expire.")

        if not self.payment_deadline.has_passed(now):
            raise BookingCannotExpireError("Booking payment deadline has not passed.")

        self.status = BookingStatus.EXPIRED

        self._domain_events.append(
            BookingExpired(
                booking_id=self.id,
                customer_id=self.customer_id,
                event_id=self.event_id,
            )
        )

    def mark_refund_required(self) -> None:
        if self.status != BookingStatus.PAID:
            raise BookingCannotBePaidError(
                "Only paid bookings can be marked as refund required."
            )

        self.refund_required = True

        for ticket in self.tickets:
            if ticket.status == TicketStatus.ACTIVE:
                ticket.mark_refund_required()

    def mark_refunded(self) -> None:
        if self.status != BookingStatus.PAID:
            raise BookingCannotBePaidError("Only paid bookings can be refunded.")

        self.status = BookingStatus.REFUNDED
        self.refund_required = False

        for ticket in self.tickets:
            if ticket.status in [TicketStatus.ACTIVE, TicketStatus.REFUND_REQUIRED]:
                ticket.cancel()

    def has_checked_in_ticket(self) -> bool:
        return any(ticket.is_checked_in() for ticket in self.tickets)

    def get_ticket_by_code(self, ticket_code: TicketCode) -> Ticket | None:
        for ticket in self.tickets:
            if ticket.ticket_code == ticket_code:
                return ticket

        return None

    def check_in_ticket(
        self,
        ticket_code: TicketCode,
        checked_in_at: datetime,
    ) -> None:
        ticket = self.get_ticket_by_code(ticket_code)

        if ticket is None:
            raise TicketCannotBeCheckedInError("Ticket code was not found in this booking.")

        ticket.check_in(checked_in_at)

        self._domain_events.append(
            TicketCheckedIn(
                ticket_id=ticket.id,
                booking_id=self.id,
                event_id=self.event_id,
                ticket_code=ticket.ticket_code,
            )
        )

    @property
    def domain_events(self):
        return list(self._domain_events)

    def clear_domain_events(self) -> None:
        self._domain_events.clear()