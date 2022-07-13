from secapi.util import (DateRange, KeyMapper, Request, JSON_FILE)
from warnings import warn

FILING_INFORMATION_KEYS = ['accessionNumber',
                           'filingDate',
                           'reportDate',
                           'acceptanceDateTime',
                           'act',
                           'form',
                           'fileNumber',
                           'filmNumber',
                           'items',
                           'size',
                           'isXBRL',
                           'isInlineXBRL',
                           'primaryDocument',
                           'primaryDocDescription']

BASE_URL_SUBMISSIONS = r'https://data.sec.gov/submissions/'

CIK_STRING = r'CIK'
REQUIRED_CIK_LENGTH = 10


class FilingQuery:

    def __init__(self):
        self._cik = None
        self._ticker_symbol = None
        self._filing_information = None
        self._form_checker = None
        self._date_range = None

        self._key_mapper = KeyMapper()


    def get_filings(self, ticker_symbol, date_from=None, date_to=None, form_types=None, filing_information=None):
        # set parsing parameters
        self._ticker_symbol = ticker_symbol
        self._cik = self._key_mapper.get_cik(ticker_symbol)
        self._date_range = DateRange(date_from=date_from, date_to=date_to)

        if form_types is not None:
            if type(form_types) is not list:
                raise ValueError('form_types must be of type list of None')

            for form_type in form_types:
                if type(form_type) is not str:
                    raise ValueError('form types must be of type str')

        self._form_checker = self.create_form_checker(form_types)

        if filing_information is None:
            self._filing_information = FILING_INFORMATION_KEYS
        else:
            # this way the ordering of the keys is always the same so the query returns consistent and easy to read data
            cache_list = []
            for key in FILING_INFORMATION_KEYS:
                if key in filing_information:
                    filing_information.remove(key)
                    cache_list.append(key)

            if len(filing_information) > 0:
                warn("filing_information list contains key that does not exist")
            self._filing_information = cache_list

        # get the main submissions file
        length_diff = REQUIRED_CIK_LENGTH - len(self._cik)
        cik = ('0' * length_diff) + self._cik
        submissions_url = BASE_URL_SUBMISSIONS + CIK_STRING + cik + JSON_FILE

        response = Request.sec_request(url=submissions_url)
        submissions_dict = response.json()
        return self._parse_submissions(submissions_dict)


    def supports_ticker(self, ticker_symbol):
        return self._key_mapper.has_cik(ticker_symbol)


    @staticmethod
    def create_form_checker(form_types):
        if form_types is None:
            return lambda form: True
        else:
            return lambda form: form in form_types


    def _parse_submissions(self, submissions_dict):
        filings = []

        # parse recent
        data = submissions_dict['filings']['recent']
        recent_date_range = DateRange(date_from=data['filingDate'][-1], date_to=data['filingDate'][0])

        if self._date_range.intersect(recent_date_range):
            filings += self._filter_filings(data)

        # parse files
        files = submissions_dict['filings']['files']
        for file in files:
            filing_date_range = DateRange(date_from=file['filingFrom'], date_to=file['filingTo'])

            if self._date_range.intersect(filing_date_range):
                url = BASE_URL_SUBMISSIONS + file['name']
                response = Request.sec_request(url=url)
                data = response.json()
                filings += self._filter_filings(data)

        return filings


    def _filter_filings(self, block_data):
        filings = []

        dates = block_data['filingDate']
        forms = block_data['form']
        for i, date, form in enumerate(zip(dates, forms)):

            if date in self._date_range and self._form_checker(form):
                filing = {'tickerSymbol': self._ticker_symbol, 'cik': self._cik}
                for key in self._filing_information:
                    filing[key] = block_data[key][i]
                filings.append(filing)

        return filings
