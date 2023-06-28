"""
This script tries to test for a data limit on the SEC API.
"""
from threading import Thread
from src.secapi_tl import get_registered_tickers, sec_request
import random


REQUIRED_CIK_LENGTH = 10
BASE_URL_SUBMISSIONS = "https://data.sec.gov/submissions/"
CIK_STRING = "CIK"
JSON_FILE = ".json"

THREAD_COUNT = 5


REQUEST_COUNT = request_count = 500
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


def thread_func():
    global request_count
    while request_count > 0:
        try:
            request_count -= 1
            data = sec_request(random.choice(URLS))
            print(f"xml ownership document size: {len(data.content)}")
            print(f"request {request_count} was successful")
        except ConnectionError as e:
            print(f"Request was not successful: {e}")
            continue


def execute1():
    threads = []
    for i in range(THREAD_COUNT):
        thread = Thread(target=thread_func)
        threads.append(thread)
        thread.start()

    return threads