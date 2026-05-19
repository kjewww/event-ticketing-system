from enum import Enum

class TicketStatus(Enum):
    DRAFT = "Draft"
    PUBLISHED = "Published"
    CANCELLED = "Canceled"
    COMPLETED = "Completed"

