from datetime import datetime
from uuid import UUID, uuid4

class TicketCategoryCreated:
    def __init__(
        self, 
        ticket_category_id: UUID
    ):
        self.ticket_category_id = ticket_category_id
        self.occurred_at = datetime.now()

class TicketCategoryDisabled:
    def __init__(
        self, 
        ticket_category_id: UUID
    ):
        self.ticket_category_id = ticket_category_id
        self.occurred_at = datetime.now()