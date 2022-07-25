from __future__ import annotations

from datetime import datetime


DATE_FORMAT = '%Y-%m-%d'


class DateBorder:

    def __lt__(self, other: DateBorder):
        pass

    def __gt__(self, other: DateBorder):
        pass

    def __eq__(self, other: DateBorder):
        pass

    def __le__(self, other: DateBorder):
        pass

    def __ge__(self, other: DateBorder):
        pass


class Date(DateBorder):

    def __init__(self, date):
        self._date = datetime.strptime(date, DATE_FORMAT)

    def __lt__(self, other):
        if isinstance(other, Date):
            return self._date < other._date
        elif isinstance(other, FromInfinity):
            return False
        elif isinstance(other, ToInfinity):
            return True

    def __gt__(self, other):
        if isinstance(other, Date):
            return self._date > other._date
        if isinstance(other, FromInfinity):
            return True
        if isinstance(other, ToInfinity):
            return False

    def __eq__(self, other):
        if isinstance(other, Date) and self._date == other._date:
            return True
        else:
            return False

    def __le__(self, other):
        return self < other or self == other

    def __ge__(self, other: DateBorder):
        return self > other or self == other


class FromInfinity(DateBorder):

    def __lt__(self, other):
        return True

    def __gt__(self, other):
        return False

    def __eq__(self, other):
        return isinstance(other, FromInfinity)

    def __le__(self, other):
        return self < other or self == other

    def __ge__(self, other):
        return self > other or self == other


class ToInfinity(DateBorder):

    def __lt__(self, other):
        return False

    def __gt__(self, other):
        return True

    def __eq__(self, other):
        return isinstance(other, ToInfinity)

    def __le__(self, other):
        return self < other or self == other

    def __ge__(self, other):
        return self > other or self == other
