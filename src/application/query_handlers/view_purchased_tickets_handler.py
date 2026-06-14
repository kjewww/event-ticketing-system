from src.application.dto.ticket_dto import PurchasedTicketDTO
from src.application.interfaces.booking_read_repository import BookingReadRepository
from src.application.queries.view_purchased_tickets_query import (
    ViewPurchasedTicketsQuery,
)


class ViewPurchasedTicketsQueryHandler:
    def __init__(
        self,
        booking_read_repository: BookingReadRepository,
    ):
        self.booking_read_repository = booking_read_repository

    def handle(
        self,
        query: ViewPurchasedTicketsQuery,
    ) -> list[PurchasedTicketDTO]:
        return self.booking_read_repository.find_purchased_tickets_by_customer(
            customer_id=query.customer_id,
        )