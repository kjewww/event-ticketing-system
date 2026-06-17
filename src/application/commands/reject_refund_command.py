from uuid import UUID


class RejectRefundCommand:
    def __init__(
        self,
        refund_id: UUID,
        organizer_id: UUID,
        rejection_reason: str,
    ):
        self.refund_id = refund_id
        self.organizer_id = organizer_id
        self.rejection_reason = rejection_reason