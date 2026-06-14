from datetime import datetime
from uuid import UUID


class ExpireBookingCommand:
    def __init__(
        self,
        booking_id: UUID,
        now: datetime,
    ):
        self.booking_id = booking_id
        self.now = now