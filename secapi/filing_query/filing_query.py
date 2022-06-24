from secapi.util.keymapper.key_mapper import KeyMapper
from secapi.filing_query.sec_constants import FORM_TYPES, FILING_INFORMATION_KEYS
from secapi.util.daterange.date_range import DateRange
from secapi.util.limiter.request_limitation import limited_request
from secapi.util.filetypes.file_types import JSON_FILE
from warnings import warn


BASE_URL_SUBMISSIONS = r'https://data.sec.gov/submissions/'
HEADER = {'User-Agent': 'myUserAgent'}

CIK_STRING = r'CIK'
REQUIRED_CIK_LENGTH = 10


class FilingQuery:

    def __init__(self):
        self.cik = None
        self.ticker_symbol = None
        self.filing_information = None
        self.form_types = None
        self.date_range = None

        self._key_mapper = KeyMapper()

    def get_filings(self, ticker_symbol, date_from=None, date_to=None, form_types=None, filing_information=None):
        # set parsing parameters
        self.ticker_symbol = ticker_symbol
        self.cik = self._key_mapper.get_cik(ticker_symbol)
        self.date_range = DateRange(date_from=date_from, date_to=date_to)

        if form_types is None:
            self.form_types = FORM_TYPES
        else:
            for form_type in form_types:
                if form_type not in FORM_TYPES:
                    warn("form_types list contains form type that either does not exist or is not supported")
                    form_types.remove(form_type)
            self.form_types = form_types

        if filing_information is None:
            self.filing_information = FILING_INFORMATION_KEYS
        else:
            # this way the ordering of the keys is always the same which is important for the parsing process
            cache_list = []
            for key in FILING_INFORMATION_KEYS:
                if key in filing_information:
                    filing_information.remove(key)
                    cache_list.append(key)

            if len(filing_information) > 0:
                warn("filing_information list contains key that does not exist")
            self.filing_information = cache_list

        # get the mains submissions file
        length_diff = REQUIRED_CIK_LENGTH - len(self.cik)
        cik = ('0' * length_diff) + self.cik
        submissions_url = BASE_URL_SUBMISSIONS + '/' + CIK_STRING + cik + JSON_FILE

        response = limited_request(url=submissions_url, header=HEADER)
        submissions_dict = response.json()

        return self._parse_submissions(submissions_dict)


    def _parse_submissions(self, submissions_dict):
        filings = []

        # parse recent
        data = submissions_dict['filings']['recent']
        recent_date_range = DateRange(date_from=data['filingDate'][-1], date_to=data['filingDate'][0])

        if self.date_range.intersect(recent_date_range):
            filings += self._filter_filings(data)

        # parse files
        files = submissions_dict['filings']['files']
        for file in files:
            filing_date_range = DateRange(date_from=file['filingFrom'], date_to=file['filingTo'])

            if self.date_range.intersect(filing_date_range):
                url = BASE_URL_SUBMISSIONS + file['name']
                response = limited_request(url=url, header=HEADER)
                data = response.json()
                filings += self._filter_filings(data)

        return filings


    def _filter_filings(self, block_data):
        filings = []

        dates = block_data['filingDate']
        forms = block_data['form']
        for i, (date, form) in enumerate(zip(dates, forms)):

            if date in self.date_range and form in self.form_types:
                filing = {'tickerSymbol': self.ticker_symbol, 'cik': self.cik}
                for key in self.filing_information:
                    filing[key] = block_data[key][i]
                filings.append(filing)

        return filings
