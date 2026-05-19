from datetime import datetime

from src.domain.entities.ticket_category import TicketCategory
from src.domain.exceptions.domain_exception import BookingNotAllowedError
from src.domain.value_objects.event_status import EventStatus


class BookingPolicy:
    def ensure_booking_allowed(
        self,
        event_status: EventStatus,
        ticket_category: TicketCategory,
        quantity: int,
        remaining_quota: int,
        has_active_booking_for_event: bool,
        requested_at: datetime,
    ) -> None:
        if event_status != EventStatus.PUBLISHED:
            raise BookingNotAllowedError(
                "Booking can only be created for a published event."
            )

        if not ticket_category.is_active:
            raise BookingNotAllowedError(
                "Booking cannot be created for an inactive ticket category."
            )

        if not ticket_category.sales_date_range.contains(requested_at):
            raise BookingNotAllowedError(
                "Booking can only be created within the ticket sales period."
            )

        if quantity <= 0:
            raise BookingNotAllowedError(
                "Ticket quantity must be greater than zero."
            )

        if quantity > remaining_quota:
            raise BookingNotAllowedError(
                "Ticket quantity exceeds remaining quota."
            )

        if has_active_booking_for_event:
            raise BookingNotAllowedError(
                "Customer already has an active booking for this event."
            )