import os
import time

from src.secapi_tl.key_mapper import is_registered
import json


GATHERING_CONFIGURATIONS_PATH = "/resources/gathering_config.json"


if __name__ == "__main__":

    with open(os.getcwd() + GATHERING_CONFIGURATIONS_PATH) as fd:
        gathering_config_dict = json.load(fd)
        # target_tickers_consumed will be destroyed at initialization of the collectors and thus should not be used
        target_tickers_consumed = gathering_config_dict["tickers"]
        start_date = gathering_config_dict["start_date"]
        number_of_collectors = gathering_config_dict["number_of_collectors"]
        number_of_aggregators = gathering_config_dict["number_of_aggregators"]

    start_time = time.time()
    number_of_requests = 0
    for ticker in target_tickers_consumed:
        number_of_requests += 1
        print(ticker)
        try:
            result = is_registered(ticker)
        except:
            break
        if not result:
            print(f"{ticker} does not exists")
            target_tickers_consumed.remove(ticker)
    end_time = time.time()

    total_time = end_time - start_time
    print(f"{number_of_requests - 1} of {len(target_tickers_consumed)} tickers were requested successful")
    print(f"requests: {number_of_requests}")
    print(f"time: {total_time}")
    print(f"requests per second: {number_of_requests / total_time}")