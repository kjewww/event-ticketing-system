from abc import ABC, abstractmethod
from uuid import UUID

from src.domain.aggregates.refund import Refund


class RefundRepository(ABC):
    @abstractmethod
    def get_by_id(self, refund_id: UUID) -> Refund | None:
        pass

    @abstractmethod
    def save(self, refund: Refund) -> None:
        pass

    @abstractmethod
    def get_by_booking_id(self, booking_id: UUID) -> Refund | None:
        pass