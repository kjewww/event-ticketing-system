from abc import ABC, abstractmethod
from uuid import UUID

from src.domain.value_objects.money import Money


class RefundPaymentService(ABC):
    @abstractmethod
    def pay_out_refund(
        self,
        refund_id: UUID,
        customer_id: UUID,
        amount: Money,
    ) -> str:
        pass