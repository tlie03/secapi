"""
This script tries to test for a data limit on the SEC API.
"""
from typing import List
from threading import Thread
from src.secapi_tl import get_registered_ciks, sec_request


REQUIRED_CIK_LENGTH = 10
BASE_URL_SUBMISSIONS = "https://data.sec.gov/submissions/"
CIK_STRING = "CIK"
JSON_FILE = ".json"

THREAD_COUNT = 5
ciks_total = get_registered_ciks()


def thread_func(ciks: List[str]):
    for i, cik in enumerate(ciks):
        length_diff = REQUIRED_CIK_LENGTH - len(cik)
        cik_formatted = ('0' * length_diff) + cik
        url = BASE_URL_SUBMISSIONS + CIK_STRING + cik_formatted + JSON_FILE
        response = sec_request(url)
        print(len(response.content))



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
