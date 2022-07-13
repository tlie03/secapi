import os
import pandas as pd


with open(os.path.dirname(os.path.realpath(__file__)) + "/valid_dates_sorted.csv") as file:
    df = pd.read_csv(file)
    valid_dates_sorted = df['dates'].tolist()


with open(os.path.dirname(os.path.realpath(__file__)) + "/invalid_dates.csv") as file:
    df = pd.read_csv(file)
    invalid_dates = df['dates'].tolist()
