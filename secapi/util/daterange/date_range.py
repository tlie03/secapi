from secapi.util.daterange.range_borders import Date, FromInfinity, ToInfinity


class DateRange:

    def __init__(self, date_from, date_to):
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
            if self._date_to < self._date_from:
                raise ValueError('date_to must be equal or greater than date_from')

    def __contains__(self, item):
        date = Date(item)
        return self._date_from <= date <= self._date_to

    def __iter__(self):
        if not self._is_finite:
            raise ValueError('can not iterate over infinite DateRange')
        else:
            iteration = self._date_from
            while iteration <= self._date_to:
                yield iteration
                iteration += 1

    def date_from(self):
        return self._date_from

    def date_to(self):
        return self._date_to

    def intersect(self, daterange):
        return not (self._date_to < daterange.date_from() or daterange.date_to() < self._date_from)