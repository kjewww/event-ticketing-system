from abc import ABC, abstractmethod
from uuid import UUID

from src.application.dto.ticket_dto import PurchasedTicketDTO


class BookingReadRepository(ABC):
    @abstractmethod
    def find_purchased_tickets_by_customer(
        self,
        customer_id: UUID,
    ) -> list[PurchasedTicketDTO]:
        pass