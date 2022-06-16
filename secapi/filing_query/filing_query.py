from secapi.util.keymapper.key_mapper import KeyMapper
from secapi.util.date.date_range import DateRange
from secapi.util.request.request_limitation import limited_request


BASE_URL_SUBMISSIONS = r'https://data.sec.gov/submissions/'
BASE_URL_ARCHIVE = r'https://www.sec.gov/Archives/edgar/data/'
HEADER = {'User-Agent': 'myUserAgent'}

FILING_TYPES = ['3', '4', '5']  # todo add filing types

CIK_STRING = 'CIK'
REQUIRED_CIK_LENGTH = 10


class FilingQuery:

    def __init__(self):
        self._key_mapper = KeyMapper()

    def get_filings(self, ticker_symbol, filing_types=None, date_from=None, date_to=None):
        if filing_types is None:
            filing_types = FILING_TYPES

        cik = self._key_mapper.get_cik(ticker_symbol)
        date_range = DateRange(date_from, date_to)
