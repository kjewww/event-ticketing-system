from src.domain.aggregates.booking import Booking
from src.domain.aggregates.event import Event


class EventCancellationService:
    def cancel_event_and_mark_paid_bookings(
        self,
        event: Event,
        paid_bookings: list[Booking],
    ) -> None:
        event.cancel()

        for booking in paid_bookings:
            booking.mark_refund_required()