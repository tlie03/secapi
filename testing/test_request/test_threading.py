import time
from threading import Thread, Lock
from secapi import Request
from testing.helper import timer


# example link
link = r'https://www.sec.gov/Archives/edgar/data/0000789019/000106299322016449/xslF345X03/form4.xml'

thread_count = 10
lock = Lock()

request_count = counter = 1000


@timer
def thread_func():
    global counter

    while counter > 0:
        lock.acquire()
        counter -= 1
        lock.release()
        response = Request.sec_request(link)
        assert response.status_code == 200


threads = [Thread(target=thread_func) for i in range(thread_count)]

t_start = time.time()

for thread in threads:
    thread.start()

for thread in threads:
    thread.join()

t_end = time.time()
total_time = t_end - t_start

print(total_time)
print(f'requests per second: {request_count/total_time}')