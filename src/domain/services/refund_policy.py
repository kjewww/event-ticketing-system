from datetime import datetime

from src.domain.aggregates.booking import Booking
from src.domain.exceptions.domain_exception import RefundNotAllowedError
from src.domain.value_objects.booking_status import BookingStatus
from src.domain.value_objects.event_status import EventStatus


class RefundPolicy:
    def ensure_refund_allowed(
        self,
        booking: Booking,
        event_status: EventStatus,
        refund_deadline: datetime,
        requested_at: datetime,
    ) -> None:
        if booking.status != BookingStatus.PAID:
            raise RefundNotAllowedError(
                "Refund can only be requested for paid booking."
            )

        if booking.has_checked_in_ticket():
            raise RefundNotAllowedError(
                "Refund cannot be requested because one or more tickets have been checked in."
            )

        if event_status == EventStatus.CANCELLED:
            return

        if requested_at > refund_deadline:
            raise RefundNotAllowedError(
                "Refund deadline has passed."
            )