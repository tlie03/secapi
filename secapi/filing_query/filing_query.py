from secapi.util.keymapper.key_mapper import KeyMapper
from secapi.util.date.date_range import DateRange
from secapi.util.request.request_limitation import limited_request
from secapi.util.filetypes.file_types import JSON_FILE


BASE_URL_SUBMISSIONS = r'https://data.sec.gov/submissions/'
BASE_URL_ARCHIVE = r'https://www.sec.gov/Archives/edgar/data/'
HEADER = {'User-Agent': 'myUserAgent'}

FILING_TYPES = ['3', '4', '5']  # todo add filing types

CIK_STRING = r'CIK'
REQUIRED_CIK_LENGTH = 10


class FilingQuery:

    def __init__(self):
        self._key_mapper = KeyMapper()

    def get_filings(self, ticker_symbol, filing_types=None, date_from=None, date_to=None):
        if filing_types is None:
            filing_types = FILING_TYPES
        cik = self._key_mapper.get_cik(ticker_symbol.upper())
        date_range = DateRange(date_from, date_to)
        submissions_dict = self._get_submissions(cik)

        return self._parse_submissions_dict(submissions_dict, date_range, filing_types)


    def _get_submissions(self, cik):
        submissions_url = self._build_submissions_url(cik)
        response = limited_request(url=submissions_url, header=HEADER)
        return response.json()

    @staticmethod
    def _build_submissions_url(cik):
        length_diff = REQUIRED_CIK_LENGTH - len(cik)
        cik = ('0' * length_diff) + cik
        return BASE_URL_SUBMISSIONS + '/' + CIK_STRING + cik + JSON_FILE

    def _parse_submissions_dict(self, submissions_dict, daterange, filings_types):
        pass
