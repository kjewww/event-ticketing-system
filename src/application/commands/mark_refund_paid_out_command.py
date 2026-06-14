from uuid import UUID


class MarkRefundPaidOutCommand:
    def __init__(
        self,
        refund_id: UUID,
        admin_id: UUID,
    ):
        self.refund_id = refund_id
        self.admin_id = admin_id