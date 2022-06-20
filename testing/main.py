import time
from secapi.filing_query.filing_query import FilingQuery
import threading
from secapi.util.request.request_limitation import limited_request


form_types = ['3', '4', '5']
filing_information = ['accessionNumber', 'filingDate', 'form']
fq = FilingQuery()
filings = fq.get_filings('MSFT', date_from='2017-12-12', date_to='2020-12-12', form_types=form_types, filing_information=filing_information)

for filing in filings:
    print(filing)
