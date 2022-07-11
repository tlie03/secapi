from datetime import datetime
from secapi.util.limiter.request import Request
import xmltodict
import re

BASE_URL_ARCHIVE = r'https://www.sec.gov/Archives/edgar/data/'
DOC_NAME_REGEX = re.compile('/.*\.xml$')


class Form4Parser:

    def __init__(self):
        self._REQUIRED_INFORMATION = ['accessionNumber', 'cik', 'primaryDocument', 'form', 'filingDate']
        self._PARSABLE_FORMS = ['4', '4/A']
        self._DATA_KEYS = ['documentType', 'issuer', 'reportingOwner', 'nonDerivativeTable', 'derivativeTable']
        self._MIN_DATE = datetime.strptime("2004-01-01", "%Y-%m-%d")


    def get_required_information(self):
        return self._REQUIRED_INFORMATION


    def get_parsable_forms(self):
        return self._PARSABLE_FORMS


    def parse_filing(self, filing):
        filing_information = filing.keys()

        for key in self._REQUIRED_INFORMATION:
            if key not in filing_information:
                raise KeyError(f'missing an required information in filing. Missing information: {key}')

        if datetime.strptime(filing['filingDate'], "%Y-%m-%d") < self._MIN_DATE:
            raise ValueError("filingDate must be greater or equal to 2004-01-01")

        if filing['form'] not in self._PARSABLE_FORMS:
            raise ValueError(f"form is not supported by this parser. from: {filing['form']}")

        try:
            accession_number = filing['accessionNumber'].replace('-', '')
            cik = filing['cik']
            doc = re.findall(DOC_NAME_REGEX, filing['primaryDocument'])[0]

            document_url = BASE_URL_ARCHIVE + cik + '/' + accession_number + '/' + doc
            response = Request.sec_request(url=document_url)
            document = xmltodict.parse(response.text)
        except:
            raise ValueError("document not parable")

        return self._reformat_document(document)


    def _reformat_document(self, document):
        data = document['ownershipDocument']

        remove_keys = [key for key in data.keys() if key not in self._DATA_KEYS]
        for key in remove_keys:
            del data[key]

        keys = data.keys()
        if 'DerivativeTable' not in keys:
            data['DerivativeTable'] = {''}

        return data
