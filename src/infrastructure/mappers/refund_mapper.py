from src.domain.aggregates.refund import Refund
from src.domain.value_objects.money import Money
from src.domain.value_objects.refund_status import RefundStatus

from src.infrastructure.database.models.refund_model import RefundModel


class RefundMapper:
    @staticmethod
    def to_domain(model: RefundModel) -> Refund:
        return Refund.reconstruct(
            id=model.id,
            booking_id=model.booking_id,
            customer_id=model.customer_id,
            amount=Money(
                amount=model.amount,
                currency=model.currency,
            ),
            reason=model.reason,
            status=RefundStatus(model.status),
            rejection_reason=model.rejection_reason,
            payment_reference=model.payment_reference,
        )

    @staticmethod
    def to_model(domain: Refund) -> RefundModel:
        return RefundModel(
            id=domain.id,
            booking_id=domain.booking_id,
            customer_id=domain.customer_id,
            amount=domain.amount.amount,
            currency=domain.amount.currency,
            reason=domain.reason,
            status=domain.status.value,
            rejection_reason=domain.rejection_reason,
            payment_reference=domain.payment_reference,
        )