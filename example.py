from secapi_tl import (get_filings, Request)
import xmltodict


BASE_URL_ARCHIVE = r'https://www.sec.gov/Archives/edgar/data/'


def build_form4_link(filing_metadata: dict) -> str:
    """
    I found out how to build the form4 links by looking at example form 4 filing
    links and trying to build them with the metadata I had for the corresponding filings.
    For other form types this function probably differs.
    """
    cik = filing_metadata['cik']
    accession_number = filing_metadata['accessionNumber'].replace("-", "")

    # only the file name is needed from the primary document sub path to get to the raw xml file
    file_name = filing_metadata['primaryDocument'].split('/')[1]
    url = BASE_URL_ARCHIVE + cik + '/' + accession_number + '/' + file_name
    return url


filings = get_filings(ticker_symbol="AAPL", date_from="2012-01-01", date_to="2012-02-01", form_types=["4"])

for filing in filings:
    filing_link = build_form4_link(filing)
    response = Request.sec_request(url=filing_link)

    xml_data = response.text
    dict_data = xmltodict.parse(xml_data)
    print(dict_data)
