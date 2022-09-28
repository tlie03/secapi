from src.secapi.request import Request

# a file maintained by the sec that holds all ticker symbols and their corresponding cik
SEC_CIK_TICKERS_DATA = r"https://www.sec.gov/files/company_tickers.json"


def get_cik(ticker_symbol):
    # gets the cik that belongs to the company with the given ticker symbol
    ticker = ticker_symbol.upper()
    response = Request.sec_request(SEC_CIK_TICKERS_DATA)
    data = response.json()

    for entry in data.values():
        if entry['ticker'] == ticker:
            return str(entry['cik_str'])
    raise ValueError(f'ticker symbol {ticker} not found')


def is_registered(ticker_symbol):
    # proofs whether the company with the given ticker symbol is registered at the sec
    ticker = ticker_symbol.upper()
    response = Request.sec_request(SEC_CIK_TICKERS_DATA)
    data = response.json()

    for entry in data:
        if entry['ticker'] == ticker:
            return True
    else:
        return False
