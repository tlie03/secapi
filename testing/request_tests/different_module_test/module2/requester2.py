from typing import List
from threading import Thread
from src.secapi_tl import get_registered_ciks, get_filings
from ratelimit import limits, sleep_and_retry


CALLS = 10
PERIOD = 1
THREAD_COUNT = 5
ciks_total = get_registered_ciks()


@sleep_and_retry
@limits(calls=CALLS, period=PERIOD)
def limited_get_filings(ticker_symbol: str) -> List[str]:
    filings = get_filings(ticker_symbol=ticker_symbol)
    return filings


def thread_func(ciks: List[str]):
    for i, cik in enumerate(ciks):
        # print(f"{i} / {len(ciks)}")
        successful = False
        while not successful:
            try:
                filings = limited_get_filings(cik)
                successful = True
            except Exception as e:
                print(e)


def execute2():
    buckets = [[] for _ in range(THREAD_COUNT)]
    for i, cik in enumerate(ciks_total):
        buckets[i % THREAD_COUNT].append(cik)

    threads = []
    for i in range(THREAD_COUNT):
        bucket = buckets[i]
        thread = Thread(target=thread_func, args=[bucket])
        threads.append(thread)
        thread.start()

    return threads
