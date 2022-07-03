from secapi.util.limiter.request_limitation import limited_request
import xmltodict

BASE_URL_ARCHIVE = r'https://www.sec.gov/Archives/edgar/data/'
HEADER = {'User-Agent': 'myUserAgent'}


class Form4Parser:

    def __init__(self):
        self._REQUIRED_INFORMATION = ['accessionNumber', 'cik', 'primaryDocument', 'form']
        self._PARSABLE_FORMS = ['4', '4/A']


    def parse_filing(self, filing):
        filing_information = filing.keys()

        for key in self._REQUIRED_INFORMATION:
            if key not in filing_information:
                raise KeyError(f'missing an required information in filing. Missing information: {key}')

        if filing['form'] not in self._PARSABLE_FORMS:
            raise ValueError(f"form is not supported by this parser. from: {filing['form']}")

        accessionNumber = filing['accessionNumber'].replace('-', '')
        cik = str(filing['cik'])
        doc_location = filing['primaryDocument']
        if doc_location.count('/') != 1:
            raise ValueError(f'invalid document location. document_location: {doc_location}')
        doc = doc_location.split('/')[1]

        document_url = BASE_URL_ARCHIVE + cik + '/' + accessionNumber + '/' + doc
        response = limited_request(url=document_url, headers=HEADER)
        document = response.text
        return self._parse_document(document)


    def _parse_document(self, document):
        xml_dict = xmltodict.parse(document)
        document = xml_dict['ownershipDocument']


    @staticmethod
    def _parse_meta(table):
        pass


    @staticmethod
    def _parse_non_derivative(table):
        pass


    @staticmethod
    def _parse_derivative(table):
        pass
