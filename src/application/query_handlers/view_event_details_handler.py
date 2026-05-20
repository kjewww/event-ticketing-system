from src.application.dto.event_dto import EventDetailsDTO
from src.application.dto.ticket_category_dto import TicketCategoryDTO
from src.application.interfaces.event_read_repository import EventReadRepository
from src.application.queries.view_event_details_query import ViewEventDetailsQuery


class ViewEventDetailsQueryHandler:
    def __init__(self, event_read_repository: EventReadRepository):
        self.event_read_repository = event_read_repository

    def handle(self, query: ViewEventDetailsQuery) -> EventDetailsDTO:
        event = self.event_read_repository.get_event_details(query.event_id)

        if event is None:
            raise ValueError("Event not found.")

        ticket_categories = [
            TicketCategoryDTO(
                ticket_category_id=category.ticket_category_id,
                name=category.name,
                price_amount=category.price_amount,
                currency=category.currency,
                quota=category.quota,
                remaining_quota=category.remaining_quota,
                sales_start_date=category.sales_start_date,
                sales_end_date=category.sales_end_date,
                is_active=category.is_active,
                purchase_status=category.purchase_status,
            )
            for category in event.ticket_categories
        ]

        return EventDetailsDTO(
            event_id=event.event_id,
            name=event.name,
            description=event.description,
            start_date=event.start_date,
            end_date=event.end_date,
            location=event.location,
            organizer_id=event.organizer_id,
            status=event.status,
            ticket_categories=ticket_categories,
        )