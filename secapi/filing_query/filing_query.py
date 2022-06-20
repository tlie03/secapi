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

    def _set_parsing_parameters(self, date_range, form_types, filing_information):
        self._date_range = date_range
        self._form_types = form_types
        self._filing_information = filing_information

    def get_filings(self, ticker_symbol, date_from=None, date_to=None, form_types=None, filing_information=None):
        cik = self._key_mapper.get_cik(ticker_symbol)
        date_range = DateRange(date_from=date_from, date_to=date_to)

        if form_types is None:
            form_types = FORM_TYPES
        else:
            for form_type in form_types:
                if form_type not in FORM_TYPES:
                    warn("form_types list contains form type that either does not exist or is not supported")
                    form_types.remove(form_type)

        if filing_information is None:
            filing_information = FILING_INFORMATION_KEYS
        else:
            # this way the ordering of the keys is always the same which is important for the parsing process
            cache_list = []
            for key in FILING_INFORMATION_KEYS:
                if key in filing_information:
                    filing_information.remove(key)
                    cache_list.append(key)
            if len(filing_information) > 0:
                warn("filing_information list contains key that does not exist")
            filing_information = cache_list

        self._set_parsing_parameters(date_range, form_types, filing_information)

        length_diff = REQUIRED_CIK_LENGTH - len(cik)
        cik = ('0' * length_diff) + cik
        submissions_url = BASE_URL_SUBMISSIONS + '/' + CIK_STRING + cik + JSON_FILE

        response = limited_request(url=submissions_url, header=HEADER)
        submissions_dict = response.json()

        return self._parse_submissions(submissions_dict)


    def _parse_submissions(self, submissions_dict):
        filings = []

        # parse recent
        recent = submissions_dict['filings']['recent']
        recent_filing_count = len(recent['accessionNumber'])
        recent_from = recent['filingDate'][recent_filing_count - 1]
        recent_to = recent['filingDate'][0]

        recent_date_range = DateRange(date_from=recent_from, date_to=recent_to)
        if self._date_range.intersect(recent_date_range):
            filings += self._filter_block_data(recent)

        # parse files
        files = submissions_dict['filings']['files']
        for file in files:
            file_from = file['filingFrom']
            file_to = file['filingTo']
            file_date_range = DateRange(date_from=file_from, date_to=file_to)

            if self._date_range.intersect(file_date_range):
                url = BASE_URL_SUBMISSIONS + file['name']
                response = limited_request(url=url, header=HEADER)
                data = response.json()
                filings += self._filter_block_data(data)

        return filings


    def _filter_block_data(self, block_data):
        filings = []

        filing_count = len(block_data['accessionNumber'])
        for i in range(filing_count):
            filing_date = block_data['filingDate'][i]
            form_type = block_data['form'][i]

            if filing_date in self._date_range and form_type in self._form_types:
                filing = {}
                for key in self._filing_information:
                    filing[key] = block_data[key][i]
                filings.append(filing)

        return filings
