import requests
import pandas as pd
from secapi import FilingQuery, Form4Parser

ARCHIVE_URL = r'https://www.sec.gov/Archives/edgar/data/'

filing_information = ['accessionNumber', 'filingDate', 'form', 'primaryDocument']
fq = FilingQuery()


def get_filings():
    return fq.get_filings('MSFT', date_from="2016-01-01", date_to="2023-12-20", form_types=['4/A', '4'],
                          filing_information=filing_information)


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



"""
filings = get_filings()
fp = Form4Parser()
c = 0
keys = []

for filing in filings:
    c += 1
    data = fp.parse_filing(filing)
    if 'nonDerivativeHolding' in data['nonDerivativeTable'].keys():
        print(build_html_link(filing))
        for key in data['nonDerivativeTable'].keys():
            print(key)
            print(data['nonDerivativeTable'][key])


    print(f'filings parsed: {c}/{len(filings)}')
    print(f'keys found: {keys}')
"""
