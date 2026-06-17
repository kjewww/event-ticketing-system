from uuid import UUID

from src.application.interfaces.refund_payment_service import RefundPaymentService
from src.domain.value_objects.money import Money


class FakeRefundPaymentService(RefundPaymentService):
    def pay_out_refund(
        self,
        refund_id: UUID,
        customer_id: UUID,
        amount: Money,
    ) -> str:
        return f"REFUND-{refund_id.hex[:12].upper()}"