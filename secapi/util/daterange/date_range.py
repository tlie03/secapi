from .range_borders import Date, FromInfinity, ToInfinity


class DateRange:
    """
    This class implements date ranges that support open borders.
    So it is possible to create date ranges that contain all dates up to
    a specific date or all dates from a specific date. Strict ranges with
    specific dates as borders are supported as well.

    The implementation does not support any kind of daytime measurement.

    The dates given as inputs must match the '%Y-%m-%d' format.
    """

    def __init__(self, date_from: str or None, date_to: str or None):
        """
        None values represent an open border.
        """
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

    def intersect(self, date_from: str or None, date_to: str or None) -> bool:
        """
        returns true if at least one date is contained in both ranges.
        """
        daterange = DateRange(date_from=date_from, date_to=date_to)
        return not (self._date_to < daterange._date_from or daterange._date_to < self._date_from)
    