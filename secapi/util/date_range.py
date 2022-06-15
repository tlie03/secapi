from datetime import datetime

DATE_FORMAT = '%Y-%m-%d'


class DateRange:

    def __init__(self, date_from, date_to):
        self._date_from = datetime.strptime(date_from, DATE_FORMAT)
        self._date_to = datetime.strptime(date_to, DATE_FORMAT)

        if self._date_to < self._date_from:
            raise ValueError('date_to must be equal or greater than date_form')


    def __contains__(self, item):
        date = datetime.strptime(item, DATE_FORMAT)
        return self._date_from <= date <= self._date_to


    def intersects(self, date_from, date_to):
        date_from = datetime.strptime(date_from, DATE_FORMAT)
        date_to = datetime.strptime(date_to, DATE_FORMAT)

        if date_to < date_from:
            raise ValueError('date_to must be equal or greater than date_form')
        return not (self._date_to < date_from or date_to < self._date_from)
