import time
from secapi.filing_query.filing_query import FilingQuery
import threading
from secapi.util.limiter.request_limitation import limited_request
from testing.helper.timer import timer


filing_information = ['accessionNumber', 'filingDate', 'form']
fq = FilingQuery()


def get_filings():
    return fq.get_filings('MSFT')


dict_ = {'a': [1, 2, 9, 7], 'b': ['2', 'asdf', '234', '2ed2'], 'c': [121.1, 132.431, 12.32, 123.3]}


