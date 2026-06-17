class PurchasedTicketDTO:
    def __init__(
        self,
        ticket_id,
        booking_id,
        event_id,
        event_name,
        ticket_category_id,
        ticket_category_name,
        ticket_code,
        status,
        checked_in_at,
    ):
        self.ticket_id = ticket_id
        self.booking_id = booking_id
        self.event_id = event_id
        self.event_name = event_name
        self.ticket_category_id = ticket_category_id
        self.ticket_category_name = ticket_category_name
        self.ticket_code = ticket_code
        self.status = status
        self.checked_in_at = checked_in_at


class CheckInTicketResponseDTO:
    def __init__(
        self,
        ticket_code,
        event_id,
        booking_id,
        status,
        checked_in_at,
    ):
        self.ticket_code = ticket_code
        self.event_id = event_id
        self.booking_id = booking_id
        self.status = status
        self.checked_in_at = checked_in_at