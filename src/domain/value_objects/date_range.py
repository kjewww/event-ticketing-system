from datetime import datetime, date

class DateRange:
    def __init__(self, start_date: date, end_date: date):
        if end_date < start_date:
            raise ValueError("End date cannot be earlier than start date.")

        self.start_date = start_date
        self.end_date = end_date

    def contains(self, target_date: date | datetime) -> bool:
        if isinstance(target_date, datetime):
            target_date = target_date.date()

        return self.start_date <= target_date <= self.end_date