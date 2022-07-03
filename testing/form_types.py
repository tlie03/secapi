import pandas as pd
import os
from secapi.filing_query.filing_query import FilingQuery

data = pd.read_csv(os.getcwd() + '/resources/SP500tickers.csv')
tickers = data['Symbol'].tolist()

fq = FilingQuery()
form_types = []
filing_count = 0

for i, ticker in enumerate(tickers):
    if fq.supports_ticker(ticker):
        filings = fq.get_filings(ticker_symbol=ticker)
        filing_count += len(filings)
        for filing in filings:
            if filing['form'] not in form_types:
                form_types.append(filing['form'])
    print(f'processed: {i/len(tickers) * 100}%')
    print(f'filings parsed: {filing_count}')

print(f'form types found: {form_types}')
print(f'total filings parsed: {filing_count}')
