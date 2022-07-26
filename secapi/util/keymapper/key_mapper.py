from secapi.util import Request

# a file maintained by the sec that holds all ticker symbols and the corresponding cik
SEC_CIK_TICKERS_DATA = r"https://www.sec.gov/files/company_tickers.json"


def get_cik(ticker_symbol):
    ticker = ticker_symbol.upper()
    response = Request.sec_request(SEC_CIK_TICKERS_DATA)
    data = response.json()

    for entry in data:
        if entry['ticker'] == ticker:
            return entry['cik_str']

    raise ValueError(f'ticker symbol {ticker} not found')


def is_registered(ticker_symbol):
    ticker = ticker_symbol.upper()
    response = Request.sec_request(SEC_CIK_TICKERS_DATA)
    data = response.json()

    for entry in data:
        if entry['ticker'] == ticker:
            return True
    return False
