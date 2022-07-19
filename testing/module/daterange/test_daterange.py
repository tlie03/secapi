import unittest
from testing.helper import valid_dates_sorted
from secapi.util import DateRange


class Test(unittest.TestCase):

    def test_invalid_inputs(self):
        for i, date1 in enumerate(valid_dates_sorted):
            for j, date2 in enumerate(valid_dates_sorted, i):
                self.assertRaises(ValueError, self.create_date_range(date2, date1))



    @staticmethod
    def create_date_range(date_from, date_to):
        DateRange(date_from, date_to)
