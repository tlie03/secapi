from secapi.util import Request


SEC_CIK_TICKERS_DATA = r"https://www.sec.gov/files/company_tickers.json"


def get_cik(ticker_symbol):
    ts = ticker_symbol.upper()
    response = Request.sec_request(SEC_CIK_TICKERS_DATA)
    data = response.json()

    for entry in data:
        if entry['ticker'] == ts:
            return entry['cik_str']

    raise ValueError(f'ticker symbol {ts} not found')


def is_registered(ticker_symbol):
    ts = ticker_symbol.upper()
    response = Request.sec_request(SEC_CIK_TICKERS_DATA)
    data = response.json()

    for entry in data:
        if entry['ticker'] == ts:
            return True

    return False
