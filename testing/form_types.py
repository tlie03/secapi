import pandas as pd
import os
from secapi import FilingQuery, Form4Parser

ARCHIVE_URL = r'https://www.sec.gov/Archives/edgar/data/'


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


data = pd.read_csv(os.getcwd() + '/resources/SP500tickers.csv')
tickers = data['Symbol'].tolist()

fq = FilingQuery()
fp = Form4Parser()

data_keys = []
ticker_counter = 0
filing_counter = 0
filing_counter_total = 0

for ticker in tickers:
    ticker_counter += 1
    filings = fq.get_filings(ticker_symbol=ticker, date_from='2021-12-12', form_types=['4', '4/A'])

    for filing in filings:
        print('-' * 50)
        filing_counter += 1
        filing_counter_total += 1
        data = fp.parse_filing(filing)
        print(build_html_link(filing))
        print(build_xml_link(filing))

        if 'nonDerivativeTable' in data.keys() and data['nonDerivativeTable'] is not None:
            for key in data['nonDerivativeTable'].keys():
                if key not in data_keys:
                    data_keys.append(key)

        print(f'tickers parsed: {ticker_counter} / {len(tickers)}')
        print(f'filings parsed: {filing_counter} / {len(filings)}')
        print(f'filings parsed total: {filing_counter_total}')
        print(data_keys)

    filing_counter = 0
