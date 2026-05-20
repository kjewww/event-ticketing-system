from datetime import date, datetime


class DateRange:
    def __init__(self, start_date: date | datetime, end_date: date | datetime):
        self.start_date = self._to_date(start_date)
        self.end_date = self._to_date(end_date)

        if self.end_date < self.start_date:
            raise ValueError("End date cannot be earlier than start date.")

    def contains(self, target_date: date | datetime) -> bool:
        target_date = self._to_date(target_date)
        return self.start_date <= target_date <= self.end_date

    @staticmethod
    def _to_date(value: date | datetime) -> date:
        if isinstance(value, datetime):
            return value.date()

        return value