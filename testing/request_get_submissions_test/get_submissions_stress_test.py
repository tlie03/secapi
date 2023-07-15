"""
When accessing url with a small amount of data the request is fast and does not cause any problems.
But when using the get_filings method from the filing_query module a 429 error is thrown.
The main difference between the two requests is the amount of data that is returned
since the get_filings method returns large json files.
This test tries to access not only many urls but also urls that return
a large amount of data using the get_filings method.
"""
from typing import List
from threading import Thread
from src.secapi_tl import get_registered_ciks, get_submissions
from ratelimit import limits, sleep_and_retry

THREAD_COUNT = 5
ciks_total = get_registered_ciks()

CALLS = 1
PERIOD = 2


@sleep_and_retry
@limits(calls=CALLS, period=PERIOD)
def limited_get_filings(ticker_symbol: str) -> List[str]:
    filings = get_submissions(ticker_symbol_or_cik=ticker_symbol)
    return filings


def thread_func(ciks: List[str]):
    for i, cik in enumerate(ciks):
        print(f"{i} / {len(ciks)}")
        filings = limited_get_filings(cik)


if __name__ == "__main__":

    cik_buckets = [[] for _ in range(THREAD_COUNT)]
    for i, cik in enumerate(ciks_total):
        cik_buckets[i % THREAD_COUNT].append(cik)

    threads = []
    for t in range(THREAD_COUNT):
        bucket = cik_buckets[t]
        thread = Thread(target=thread_func, args=[bucket])
        threads.append(thread)
        thread.start()

    for thread in threads:
        thread.join()
