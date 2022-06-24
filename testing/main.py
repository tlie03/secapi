import time
import xmltodict
import requests
from bs4 import BeautifulSoup

from secapi.filing_query.filing_query import FilingQuery
import threading
from secapi.util.limiter.request_limitation import limited_request
from testing.helper.timer import timer
import yfinance as yf

ARCHIVE_URL = r'https://www.sec.gov/Archives/edgar/data/'

filing_information = ['accessionNumber', 'filingDate', 'form', 'primaryDocument']
fq = FilingQuery()


@timer
def get_filings():
    return fq.get_filings('TSLA', date_from="2015-01-01", date_to="2021-12-20", filing_information=filing_information)


def build_link(f):
    acn = f['accessionNumber'].replace('-', '')
    doc = f['primaryDocument']
    cik = f['cik']
    return ARCHIVE_URL + cik + '/' + acn + '/' + doc


filings = get_filings()
filing_link = build_link(filings[-1])
print(filing_link)

response = requests.get(url=filing_link, headers={'User-Agent': 'myUserAgent'})
soup = BeautifulSoup(response.text, 'lxml')
body = soup.find('body')
print(body.prettify())
