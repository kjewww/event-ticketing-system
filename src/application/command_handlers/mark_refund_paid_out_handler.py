from src.application.commands.mark_refund_paid_out_command import (
    MarkRefundPaidOutCommand,
)
from src.application.dto.refund_dto import MarkRefundPaidOutResponseDTO
from src.application.interfaces.refund_payment_service import RefundPaymentService
from src.application.interfaces.unit_of_work import UnitOfWork

from src.domain.exceptions.domain_exception import RefundStatusError
from src.domain.repositories.refund_repository import RefundRepository
from src.domain.value_objects.refund_status import RefundStatus


class MarkRefundPaidOutCommandHandler:
    def __init__(
        self,
        refund_repository: RefundRepository,
        refund_payment_service: RefundPaymentService,
        unit_of_work: UnitOfWork,
    ):
        self.refund_repository = refund_repository
        self.refund_payment_service = refund_payment_service
        self.unit_of_work = unit_of_work

    def handle(
        self,
        command: MarkRefundPaidOutCommand,
    ) -> MarkRefundPaidOutResponseDTO:
        try:
            refund = self.refund_repository.get_by_id(command.refund_id)

            if refund is None:
                raise ValueError("Refund not found.")

            if refund.status != RefundStatus.APPROVED:
                raise RefundStatusError(
                    "Only approved refunds can be marked as paid out."
                )

            payment_reference = self.refund_payment_service.pay_out_refund(
                refund_id=refund.id,
                customer_id=refund.customer_id,
                amount=refund.amount,
            )

            refund.mark_paid_out(payment_reference)

            self.refund_repository.save(refund)
            self.unit_of_work.commit()

            return MarkRefundPaidOutResponseDTO(
                refund_id=refund.id,
                booking_id=refund.booking_id,
                status=refund.status.value,
                payment_reference=refund.payment_reference,
            )

        except Exception:
            self.unit_of_work.rollback()
            raise