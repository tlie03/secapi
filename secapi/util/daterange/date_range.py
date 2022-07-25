from .range_borders import Date, FromInfinity, ToInfinity


class DateRange:

    def __init__(self, date_from: str, date_to: str):
        if date_from is None:
            self._date_from = FromInfinity()
        else:
            self._date_from = Date(date_from)

        if date_to is None:
            self._date_to = ToInfinity()
        else:
            self._date_to = Date(date_to)

        self._is_finite = not (date_from is None or date_to is None)

        if self._is_finite:
            if self._date_to <= self._date_from:
                raise ValueError('date_to must be equal or greater than date_from')

    def __contains__(self, item: str):
        date = Date(item)
        return self._date_from <= date <= self._date_to

    def intersect(self, date_from: str, date_to: str) -> bool:
        daterange = DateRange(date_from=date_from, date_to=date_to)
        return not (self._date_to < daterange._date_from or daterange._date_to < self._date_from)