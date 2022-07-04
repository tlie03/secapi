import requests
import pandas as pd
from secapi.filing_query.filing_query import FilingQuery
from testing.helper.timer import timer
import xmltodict



ARCHIVE_URL = r'https://www.sec.gov/Archives/edgar/data/'

filing_information = ['accessionNumber', 'filingDate', 'form', 'primaryDocument']
fq = FilingQuery()


def get_filings():
    return fq.get_filings('AAPL', date_from="2004-01-01", date_to="2023-12-20", form_types=['4'], filing_information=filing_information)


def build_xml_link(f):
    acn = f['accessionNumber'].replace('-', '')
    doc = f['primaryDocument'].split('/')[1]
    cik = f['cik']
    return ARCHIVE_URL + cik + '/' + acn + '/' + doc


def build_html_link(f):
    acn = f['accessionNumber'].replace('-', '')
    doc = f['primaryDocument']
    cik = f['cik']
    return ARCHIVE_URL + cik + '/' + acn + '/' + doc


filings = get_filings()
filing = filings[-20]

filing_link = build_xml_link(filing)
print(build_html_link(filing))
print(filing_link)

response = requests.get(url=filing_link, headers={'User-Agent': 'myUserAgent'})

