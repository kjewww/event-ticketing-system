class CreateTicketCategoryResponseDTO:
    def __init__(
        self,
        event_id,
        ticket_category_id,
        name,
        price_amount,
        currency,
        quota,
        sales_start_date,
        sales_end_date,
        is_active,
    ):
        self.event_id = event_id
        self.ticket_category_id = ticket_category_id
        self.name = name
        self.price_amount = price_amount
        self.currency = currency
        self.quota = quota
        self.sales_start_date = sales_start_date
        self.sales_end_date = sales_end_date
        self.is_active = is_active