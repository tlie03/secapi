import random
import unittest
import secapi
from testing.helper import valid_dates_sorted, filing_information_keys, ticker_symbols
from secapi.util import DateRange


class FilingQueryTests(unittest.TestCase):

    def test_dates_results(self):
        for i in range(20):
            date_from = random.choice(valid_dates_sorted)
            index = valid_dates_sorted.index(date_from)
            date_to = random.choice(valid_dates_sorted[index:])

            ticker = random.choice(ticker_symbols)
            date_range = DateRange(date_from=date_from, date_to=date_to)
            filings = secapi.get_filings(ticker, date_from=date_from, date_to=date_to)

            for filing in filings:
                filing_date = filing['filingDate']
                self.assertTrue(filing_date in date_range)


    def test_information_keys(self):
        for i in range(20):
            keys = random.choices(filing_information_keys, k=random.randint(0, len(filing_information_keys)))
            keys = list(dict.fromkeys(keys))

            date_from = random.choice(valid_dates_sorted)
            index = valid_dates_sorted.index(date_from)
            date_to = random.choice(valid_dates_sorted[index:])

            ticker = random.choice(ticker_symbols)
            filings = secapi.get_filings(ticker, date_from, date_to, filing_information=keys)

            keys = keys + ["tickerSymbol", 'cik']
            keys.sort()
            for filing in filings:
                filing_keys = list(filing.keys())
                filing_keys.sort()
                self.assertTrue(keys == filing_keys)


    def test_form_check(self):
        for i in range(20):
            date_from = random.choice(valid_dates_sorted)
            index = valid_dates_sorted.index(date_from)
            date_to = random.choice(valid_dates_sorted[index:])

            ticker = random.choice(ticker_symbols)
            filings = secapi.get_filings(ticker, date_from=date_from, date_to=date_to, form_types=['4'])

            for filing in filings:
                form_type = filing['form']
                self.assertTrue(form_type == '4')