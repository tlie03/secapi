import requests
import pandas as pd
import os

SEC_CIK_TICKERS_DATA = r"https://www.sec.gov/files/company_tickers.json"

data = requests.get(SEC_CIK_TICKERS_DATA).json()


cik = []
ticker = []
title = []


for d in data.values():
    cik.append(d['cik_str'])
    ticker.append(d['ticker'])
    title.append(d['title'])

data_dict = {"cik": cik, "ticker": ticker, "title": title}

df = pd.DataFrame.from_dict(data_dict)
df.to_csv(os.getcwd() + "registered_companies.csv")