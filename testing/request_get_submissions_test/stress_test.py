import random

from src.secapi_tl.request import sec_request
from src.secapi_tl.submission_query import get_submissions
from src.secapi_tl.key_mapper import get_registered_tickers
from threading import Thread
from testing.helper.timer import timer
import time

REQUEST_COUNT = request_count = 500
THREAD_COUNT = 10
FORM_TYPES = ["3", "4", "5", "3/A", "4/A", "5/A"]
URLS = [
    "https://www.sec.gov/Archives/edgar/data/1018724/000112760223012687/xslF345X04/form4.xml",
    "https://www.sec.gov/Archives/edgar/data/1018724/000112760223012687/xslF345X04/form4.xml",
    "https://www.sec.gov/Archives/edgar/data/1018724/000112760223012687/xslF345X04/form4.xml",
    "https://www.sec.gov/Archives/edgar/data/1018724/000112760223011192/xslF345X04/form4.xml",
    "https://www.sec.gov/Archives/edgar/data/1018724/000112760223011192/xslF345X04/form4.xml",
    "https://www.sec.gov/Archives/edgar/data/1018724/000110465923042198/xslF345X04/tm2311443-1_4seq1.xml",
    "https://www.sec.gov/Archives/edgar/data/1018724/000110465923028442/xslF345X03/tm238276-2_4seq1.xml",
    "https://www.sec.gov/Archives/edgar/data/1018724/000110465923028442/xslF345X03/tm238276-2_4seq1.xml",
    "https://www.sec.gov/Archives/edgar/data/1018724/000110465923028445/xslF345X03/tm238276-1_4seq1.xml",
    "https://www.sec.gov/Archives/edgar/data/1018724/000112760223007056/xslF345X03/form4.xml",
    "https://www.sec.gov/Archives/edgar/data/1018724/000112760223007056/xslF345X03/form4.xml",
]
TICKERS = get_registered_tickers()


@timer
def thread_function():
    global request_count
    while request_count > 0:
        try:
            request_count -= 1
            random_number = random.randint(0, 10)
            if random_number % 2 == 0:
                data = sec_request(random.choice(URLS))
                print(f"xml ownership document size: {len(data.content)}")
            else:
                data = get_submissions(random.choice(TICKERS))
            print(f"request {request_count} was successful")
        except ConnectionError as e:
            print(f"Request was not successful: {e}")
            continue


if __name__ == "__main__":
    threads = []
    for i in range(THREAD_COUNT):
        threads.append(Thread(target=thread_function))

    start_time = time.time()

    for thread in threads:
        thread.start()

    for thread in threads:
        thread.join()

    end_time = time.time()

    print(f"total time: {end_time - start_time}")
    print(f"number of requests: {REQUEST_COUNT}")
    print(f"requests per secound: {REQUEST_COUNT / (end_time - start_time)}")
