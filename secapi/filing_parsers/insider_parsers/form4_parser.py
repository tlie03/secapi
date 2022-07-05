import re

from secapi.util.limiter.request_limitation import limited_request
import xmltodict
import re

BASE_URL_ARCHIVE = r'https://www.sec.gov/Archives/edgar/data/'
HEADER = {'User-Agent': 'myUserAgent'}
DOC_NAME_REGEX = re.compile('/.*\.xml$')


class Form4Parser:

    def __init__(self):
        self._REQUIRED_INFORMATION = ['accessionNumber', 'cik', 'primaryDocument', 'form']
        self._PARSABLE_FORMS = ['4', '4/A']
        self._DATA_KEYS = ['documentType', 'issuer', 'reportingOwner', 'nonDerivativeTable', 'derivativeTable']


    def get_required_information(self):
        return self._REQUIRED_INFORMATION


    def get_parsable_forms(self):
        return self._PARSABLE_FORMS


    def parse_filing(self, filing):
        filing_information = filing.keys()

        for key in self._REQUIRED_INFORMATION:
            if key not in filing_information:
                raise KeyError(f'missing an required information in filing. Missing information: {key}')

        if filing['form'] not in self._PARSABLE_FORMS:
            raise ValueError(f"form is not supported by this parser. from: {filing['form']}")

        accession_number = filing['accessionNumber'].replace('-', '')
        cik = filing['cik']
        doc = re.findall(DOC_NAME_REGEX, filing['primaryDocument'])[0]

        document_url = BASE_URL_ARCHIVE + cik + '/' + accession_number + '/' + doc
        response = limited_request(url=document_url, header=HEADER)
        document = xmltodict.parse(response.text)
        print(document)
        return self._reformat_document(document)


    def _reformat_document(self, document):
        data = document['ownershipDocument']

        remove_keys = [key for key in data.keys() if key not in self._DATA_KEYS]
        for key in remove_keys:
            del data[key]

        return data