from abc import ABC, abstractmethod
from uuid import UUID

from src.domain.aggregates.booking import Booking


class BookingRepository(ABC):
    @abstractmethod
    def get_by_id(self, booking_id: UUID) -> Booking | None:
        pass

    @abstractmethod
    def save(self, booking: Booking) -> None:
        pass

    @abstractmethod
    def has_active_booking_for_event(
        self,
        customer_id: UUID,
        event_id: UUID,
    ) -> bool:
        pass

    @abstractmethod
    def get_paid_bookings_by_event_id(
        self,
        event_id: UUID,
    ) -> list[Booking]:
        pass