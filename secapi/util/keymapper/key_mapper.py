import pandas as pd
import os


FILE_NAME = 'ticker_to_cik_mapping.csv'
DATA_DIRECTORY = os.path.dirname(os.path.realpath(__file__)) + '/' + 'resources'
CIK_COLUMN = 'cik'


class KeyMapper:

    def __init__(self):
        self._data = pd.read_csv(DATA_DIRECTORY + '/' + FILE_NAME)


    def get_cik(self, ticker_symbol):
        if self.has_cik(ticker_symbol):
            cik = self._data.at[ticker_symbol, CIK_COLUMN]
            return str(cik)
        else:
            raise IndexError('ticker-symbol not found')


    def has_cik(self, ticker_symbol):
        return ticker_symbol in self._data.index


    def update_cik_list(self):
        pass  # todo implement