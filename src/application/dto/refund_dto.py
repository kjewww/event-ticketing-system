class RequestRefundResponseDTO:
    def __init__(
        self,
        refund_id,
        booking_id,
        customer_id,
        amount,
        currency,
        status,
        reason,
    ):
        self.refund_id = refund_id
        self.booking_id = booking_id
        self.customer_id = customer_id
        self.amount = amount
        self.currency = currency
        self.status = status
        self.reason = reason


class ApproveRefundResponseDTO:
    def __init__(
        self,
        refund_id,
        booking_id,
        status,
    ):
        self.refund_id = refund_id
        self.booking_id = booking_id
        self.status = status


class RejectRefundResponseDTO:
    def __init__(
        self,
        refund_id,
        booking_id,
        status,
        rejection_reason,
    ):
        self.refund_id = refund_id
        self.booking_id = booking_id
        self.status = status
        self.rejection_reason = rejection_reason


class MarkRefundPaidOutResponseDTO:
    def __init__(
        self,
        refund_id,
        booking_id,
        status,
        payment_reference,
    ):
        self.refund_id = refund_id
        self.booking_id = booking_id
        self.status = status
        self.payment_reference = payment_reference