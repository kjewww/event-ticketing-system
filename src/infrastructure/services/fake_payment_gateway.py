from uuid import UUID

from src.application.interfaces.payment_gateway import PaymentGateway
from src.domain.value_objects.money import Money


class FakePaymentGateway(PaymentGateway):
    def process_payment(
        self,
        booking_id: UUID,
        customer_id: UUID,
        amount: Money,
    ) -> str:
        return f"PAY-{booking_id.hex[:12].upper()}"