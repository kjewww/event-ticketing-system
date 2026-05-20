from datetime import date, datetime


class ViewAvailableEventsQuery:
    def __init__(
        self,
        date_filter: date | datetime | None = None,
        location: str | None = None,
    ):
        self.date_filter = date_filter
        self.location = location