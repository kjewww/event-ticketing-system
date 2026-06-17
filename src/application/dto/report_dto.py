class TicketCategorySalesDTO:
    def __init__(
        self,
        ticket_category_id,
        ticket_category_name,
        tickets_sold,
    ):
        self.ticket_category_id = ticket_category_id
        self.ticket_category_name = ticket_category_name
        self.tickets_sold = tickets_sold


class BookingStatusCountDTO:
    def __init__(
        self,
        status,
        count,
    ):
        self.status = status
        self.count = count


class EventSalesReportDTO:
    def __init__(
        self,
        event_id,
        tickets_sold_per_category,
        booking_status_counts,
        total_revenue_amount,
        currency,
    ):
        self.event_id = event_id
        self.tickets_sold_per_category = tickets_sold_per_category
        self.booking_status_counts = booking_status_counts
        self.total_revenue_amount = total_revenue_amount
        self.currency = currency


class EventParticipantDTO:
    def __init__(
        self,
        customer_id,
        customer_name,
        ticket_category_name,
        ticket_code,
        check_in_status,
    ):
        self.customer_id = customer_id
        self.customer_name = customer_name
        self.ticket_category_name = ticket_category_name
        self.ticket_code = ticket_code
        self.check_in_status = check_in_status