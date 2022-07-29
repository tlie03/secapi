from typing import List
from warnings import warn

from secapi.util import (DateRange, Request, JSON_FILE, get_cik, is_registered)

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



def supports_ticker(ticker_symbol: str) -> bool:
    return is_registered(ticker_symbol.upper())


def get_filings(ticker_symbol: str,
                date_from: str = None,
                date_to: str = None,
                form_types: List[str] = None,
                filing_information: List[str] = None) -> List[dict]:

    search_daterange = DateRange(date_from=date_from, date_to=date_to)
    checker = create_filing_checker(search_daterange, form_types)
    if filing_information is None:
        information_keys = FILING_INFORMATION_KEYS
    else:
        information_keys = [i for i in FILING_INFORMATION_KEYS if i in filing_information]
        if len(information_keys) < len(filing_information):
            warn("filing_information list contains key that does not exist")


    # get the main submissions file
    cik = get_cik(ticker_symbol.upper())
    length_diff = REQUIRED_CIK_LENGTH - len(cik)
    cik_formatted = ('0' * length_diff) + cik
    submissions_url = BASE_URL_SUBMISSIONS + CIK_STRING + cik_formatted + JSON_FILE

    response = Request.sec_request(url=submissions_url)
    if response.status_code != 200:
        raise ConnectionError(f'invalid response status code, status code: {response.status_code}')

    submissions_dict = response.json()

    filings = []

    # parse recent
    data = submissions_dict['filings']['recent']

    if search_daterange.intersect(date_from=data['filingDate'][-1], date_to=data['filingDate'][0]):
        filings += filter_filings(data, checker, information_keys, cik, ticker_symbol)

    # parse files
    files = submissions_dict['filings']['files']
    for file in files:

        if search_daterange.intersect(date_from=file['filingFrom'], date_to=file['filingTo']):
            url = BASE_URL_SUBMISSIONS + file['name']
            response = Request.sec_request(url=url)
            data = response.json()
            filings += filter_filings(data, checker, information_keys, cik, ticker_symbol)

    return filings


def filter_filings(block_data, checker, information, cik, ticker_symbol):
    filings = []

    dates = block_data['filingDate']
    forms = block_data['form']
    for i, (date, form) in enumerate(zip(dates, forms)):

        if checker(date, form):
            filing = {'tickerSymbol': ticker_symbol, 'cik': cik}
            for key in information:
                filing[key] = block_data[key][i]
            filings.append(filing)
    return filings


def create_filing_checker(date_range, form_types):
    def filing_checker(filing_date, form):
        return filing_date in date_range and (form_types is None or form in form_types)
    return filing_checker
