from abc import ABC, abstractmethod
from uuid import UUID

from src.domain.value_objects.money import Money


class PaymentGateway(ABC):
    @abstractmethod
    def process_payment(
        self,
        booking_id: UUID,
        customer_id: UUID,
        amount: Money,
    ) -> str:
        pass