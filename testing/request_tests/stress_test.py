from src.secapi_tl.request import Request
from threading import Thread
from testing.helper.timer import timer
import time

example_url = "https://www.sec.gov/Archives/edgar/data/104169/000112760222022911/xslF345X03/form4.xml"

REQUEST_COUNT = request_count = 500
THREAD_COUNT = 6


@timer
def thread_function():
    global request_count

    while request_count > 0:

        try:
            response = Request.sec_request(url=example_url)
        except ConnectionError as e:
            print(f"Request was not successful: {e}")
            continue
        if response.status_code == 200:
            request_count -= 1
            print(f"{REQUEST_COUNT - request_count} request was successful")
        else:
            print(f"different status code: {response.status_code}")


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