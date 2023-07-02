from typing import List
from warnings import warn
from openDateRange import DateRange
import re

from .request import sec_request
from .key_mapper import ticker_to_cik
from .filing import Filing

# list of keys for all existing metadata points
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

JSON_FILE = ".json"
BASE_URL_SUBMISSIONS = r'https://data.sec.gov/submissions/'

CIK_STRING = r'CIK'
REQUIRED_CIK_LENGTH = 10
CIK_REGEX = re.compile('\d{0,10}')



def get_filings(ticker_symbol: str,
                date_from: str = None,
                date_to: str = None,
                form_types: List[str] = None,
                filing_information: List[str] = None) -> List[Filing]:
    """
    Returns a list of filings that match the specified parameters.
    The filings are returned as Filing objects.
    WARNING: Excessive use of this function can lead to 429 errors.
             Even though the function uses the secapi_tl.request method for its requests.
             This is probably because the sec considers many requests to the https://data.sec.gov/submissions/ url
             as a scripted bot and thus blocks requests to such urls.
             I did not set an additional rate limit to this function. If this function is used excessively,
             and causes problems it might be necessary to set a rate limit to this function.

    :param ticker_symbol: ticker symbol of the company can also be the cik of the company (str)
    :param date_from: date from which the filings should be returned
    :param date_to: date to which the filings should be returned
    :param form_types: list of form types that should be returned
    :param filing_information: list of metadata points that should be returned.
           If not set, all metadata points are returned.

    :return: list of filings that match the set parameters
    """

    search_daterange = DateRange(date_from=date_from, date_to=date_to)
    checker = create_filing_checker(search_daterange, form_types)
    if filing_information is None:
        information_keys = FILING_INFORMATION_KEYS
    else:
        information_keys = [i for i in FILING_INFORMATION_KEYS if i in filing_information]
        # proofs if the filing_information parameter contains metadata points that do not exist
        if len(information_keys) < len(filing_information):
            warn("filing_information list contains key that does not exist")

    # get the main submissions file
    # the ticker symbol can also be a cik
    if CIK_REGEX.fullmatch(ticker_symbol):
        cik = ticker_symbol
    else:
        cik = ticker_to_cik(ticker_symbol)
    length_diff = REQUIRED_CIK_LENGTH - len(cik)
    cik_formatted = ('0' * length_diff) + cik
    submissions_url = BASE_URL_SUBMISSIONS + CIK_STRING + cik_formatted + JSON_FILE

    response = sec_request(url=submissions_url)
    submissions_dict = response.json()

    filings = []
    # parse recent
    data = submissions_dict['filings']['recent']
    if search_daterange.intersects(date_from=data['filingDate'][-1], date_to=data['filingDate'][0]):
        filings += filter_filings(data, checker, information_keys, cik, ticker_symbol)

    # parse files
    files = submissions_dict['filings']['files']
    for file in files:
        if search_daterange.intersects(date_from=file['filingFrom'], date_to=file['filingTo']):
            url = BASE_URL_SUBMISSIONS + file['name']
            response = sec_request(url=url)
            data = response.json()
            filings += filter_filings(data, checker, information_keys, cik, ticker_symbol)

    return [Filing.from_dict(filing_dict=filing) for filing in filings]


def filter_filings(raw_filings, checker, required_information, cik, ticker_symbol):
    filings = []

    dates = raw_filings['filingDate']
    forms = raw_filings['form']
    for i, (date, form) in enumerate(zip(dates, forms)):
        if checker(date, form):
            filing = {'tickerSymbol': ticker_symbol.upper(), 'cik': cik}
            for key in required_information:
                filing[key] = raw_filings[key][i]
            filings.append(filing)
    return filings


def create_filing_checker(date_range, form_types):
    def filing_checker(filing_date, form):
        return filing_date in date_range and (form_types is None or form in form_types)
    return filing_checker
