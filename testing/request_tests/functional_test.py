from unittest import TestCase

from datetime import datetime
from datetime import date

from src.secapi_tl import get_filings, is_registered, filter_tickers

class RequestFilings(TestCase):
    test_tickers = ["AAPL",
                    "msft",
                    "adsfa",
                    "TSLa"]

    def test_filing_amounts(self):
        filings = get_filings(ticker_symbol="COST", form_types="4", date_from="2021-03-09", date_to="2021-12-12")
        self.assertEqual(len(filings), 31)

    def test_filing_contents_types(self):
        filings = get_filings(ticker_symbol="COST", form_types=["4"], date_from="2021-03-09", date_to="2021-12-12")
        for filing in filings:
            self.assertEqual(type(filing.accession_number), str)
            self.assertEqual(type(filing.ticker_symbol), str)
            self.assertEqual(type(filing.cik), str)
            self.assertEqual(type(filing.filing_date), date)
            self.assertEqual(type(filing.report_date), date)
            self.assertEqual(type(filing.acceptance_date_time), datetime)
            self.assertEqual(type(filing.act), str)
            self.assertEqual(type(filing.form), str)
            self.assertEqual(type(filing.file_number), str)
            self.assertEqual(type(filing.film_number), str)
            self.assertEqual(type(filing.items), str)
            self.assertEqual(type(filing.size), int)
            self.assertEqual(type(filing.is_xbrl), bool)
            self.assertEqual(type(filing.is_inline_xbrl), bool)
            self.assertEqual(type(filing.primary_document), str)
            self.assertEqual(type(filing.primary_doc_description), str)

    def test_DISCK(self):
        self.assertFalse(is_registered("DISCK"))
        #filings = get_filings(ticker_symbol="DISCK", form_types=["4"])

    def test_filter_tickers(self):
        filtered_tickers = filter_tickers(RequestFilings.test_tickers)
        self.assertEqual(filtered_tickers, ["AAPL", "MSFT", "TSLA"])

