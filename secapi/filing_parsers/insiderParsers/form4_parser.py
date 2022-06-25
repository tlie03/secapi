from secapi.util.limiter.request_limitation import limited_request
from bs4 import BeautifulSoup


BASE_URL_ARCHIVE = r'https://www.sec.gov/Archives/edgar/data/'
HEADER = {'User-Agent': 'myUserAgent'}


class Form4Parser:

    def __init__(self):
        self._REQUIRED_INFORMATION = ['accessionNumber', 'cik', 'primaryDocument', 'form']
        self._PARSABLE_FORMS = ['4']


    def parse_filing(self, filing):
        filing_information = filing.keys()

        for key in self._REQUIRED_INFORMATION:
            if key not in filing_information:
                raise KeyError(f'missing an required information in filing. Missing information: {key}')

        filing_form = filing['form']
        if filing_form not in self._PARSABLE_FORMS:
            raise ValueError(f'filing form is {filing_form} which is not supported by this parser')

        accessionNumber = filing['accessionNumber'].replace('-', '')
        cik = str(filing['cik'])
        doc_location = filing['primaryDocument']

        document_url = BASE_URL_ARCHIVE + cik + '/' + accessionNumber + '/' + doc_location
        response = limited_request(url=document_url, headers=HEADER)
        document = response.text
        return self._parse_document(document)


    def _parse_document(self, document):
        soup = BeautifulSoup(document)
        body = soup.find('body')

        tables = soup.findChildren('table', recursive=False)
        meta_data = self._parse_meta(tables[1])
        non_derivative_data = self._parse_non_derivative(tables[2])
        derivative_data = self._parse_derivative(tables[3])

        return {'meta': meta_data, 'non_derivative': non_derivative_data, 'derivative': derivative_data}


    @staticmethod
    def _parse_meta(table):
        pass


    @staticmethod
    def _parse_non_derivative(table):
        pass


    @staticmethod
    def _parse_derivative(table):
        pass

