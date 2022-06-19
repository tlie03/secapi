from secapi.util.sec.key_mapper import KeyMapper
from secapi.util.sec.constants import FORM_TYPES, FILING_INFORMATION_KEYS
from secapi.util.date.date_range import DateRange
from secapi.util.request.request_limitation import limited_request
from secapi.util.filetypes.file_types import JSON_FILE
from warnings import warn


BASE_URL_SUBMISSIONS = r'https://data.sec.gov/submissions/'
BASE_URL_ARCHIVE = r'https://www.sec.gov/Archives/edgar/data/'
HEADER = {'User-Agent': 'myUserAgent'}

CIK_STRING = r'CIK'
REQUIRED_CIK_LENGTH = 10


class FilingQuery:

    def __init__(self):
        self._key_mapper = KeyMapper()

    def get_filings(self, ticker_symbol, date_from=None, date_to=None, form_types=None, filing_information=None):
        cik = self._key_mapper.get_cik(ticker_symbol)
        daterange = DateRange(date_from=date_from, date_to=date_to)

        if form_types is None:
            form_types = FORM_TYPES
        else:
            for form_type in form_types:
                if form_type not in FORM_TYPES:
                    warn("form_types list contains form types that either do not exist or are not supported")
                    form_types.remove(form_type)

        if filing_information is None:
            filing_information = FILING_INFORMATION_KEYS
        else:
            # this way the ordering of the keys is always the same which is important for the parsing process
            cache_list = []
            for key in FILING_INFORMATION_KEYS:
                if key in filing_information:
                    cache_list.append(filing_information.remove(key))
            if len(filing_information) > 0:
                warn("filing_information list contained keys that do not exist")
            filing_information = cache_list

        length_diff = REQUIRED_CIK_LENGTH - len(cik)
        cik = ('0' * length_diff) + cik
        submissions_url = BASE_URL_SUBMISSIONS + '/' + CIK_STRING + cik + JSON_FILE

        response = limited_request(url=submissions_url, header=HEADER)
        submissions_dict = response.json

        return self._parse_submissions(submissions_dict, daterange, form_types, filing_information)


    @staticmethod
    def _parse_submissions(submissions_dict, daterange, form_types, filing_information):
        # parse recent
        recent = submissions_dict['recent']
        recent_filing_count = len(recent['accessionNumber'])
        recent_from = recent['filingDate'][recent_filing_count - 1]
        recent_to = recent['filingDate'][0]

        recent_date_range = DateRange(date_from=recent_from, date_to=recent_to)
        if daterange.intersect(recent_date_range):
            for i in range(recent_filing_count):
                pass
