from datetime import datetime, date

class DateRange:
    def __init__(self, start_date: date, end_date: date):
        
        if end_date < start_date:
            raise ValueError("Start date must be before end date.")
        
        self.start_date = start_date
        self.end_date = end_date