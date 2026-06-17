from uuid import UUID


class ApproveRefundCommand:
    def __init__(
        self,
        refund_id: UUID,
        organizer_id: UUID,
    ):
        self.refund_id = refund_id
        self.organizer_id = organizer_id