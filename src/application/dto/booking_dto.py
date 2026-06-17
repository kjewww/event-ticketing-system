class CreateBookingResponseDTO:
    def __init__(
        self,
        booking_id,
        customer_id,
        event_id,
        ticket_category_id,
        quantity,
        total_price_amount,
        currency,
        payment_deadline_at,
        status,
    ):
        self.booking_id = booking_id
        self.customer_id = customer_id
        self.event_id = event_id
        self.ticket_category_id = ticket_category_id
        self.quantity = quantity
        self.total_price_amount = total_price_amount
        self.currency = currency
        self.payment_deadline_at = payment_deadline_at
        self.status = status


class PayBookingResponseDTO:
    def __init__(
        self,
        booking_id,
        status,
        total_price_amount,
        currency,
        ticket_codes,
        payment_reference,
    ):
        self.booking_id = booking_id
        self.status = status
        self.total_price_amount = total_price_amount
        self.currency = currency
        self.ticket_codes = ticket_codes
        self.payment_reference = payment_reference


class ExpireBookingResponseDTO:
    def __init__(
        self,
        booking_id,
        status,
    ):
        self.booking_id = booking_id
        self.status = status