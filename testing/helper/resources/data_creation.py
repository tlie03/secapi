import os
import random

import pandas as pd
from datetime import datetime, timedelta

cwd = os.getcwd()

date = datetime.strptime("1980-01-01", '%Y-%m-%d')
data = []
for i in range(1000):
    data.append(date.strftime('%Y-%m-%d'))
    delta = random.randint(1, 43)
    date += timedelta(delta)

print(data)
df = pd.DataFrame.from_dict({"dates": data})
print(df)
df.to_csv(cwd + "/valid_dates_sorted.csv")
