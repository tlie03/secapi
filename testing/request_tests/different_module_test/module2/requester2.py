from typing import List
from threading import Thread
from src.secapi_tl import get_registered_ciks, get_filings

THREAD_COUNT = 5
ciks_total = get_registered_ciks()


def thread_func(ciks: List[str]):
    for i, cik in enumerate(ciks):
        print(f"{i} / {len(ciks)}")
        filings = get_filings(ticker_symbol=cik)
        print(len(filings))


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
