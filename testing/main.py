import time

import threading
from secapi.util.request.request_limitation import limited_request
from testing.helper.timer import timer

URL = r'https://www.sec.gov/edgar/browse/?CIK=789019&owner=exclude'
HEADER = {'User-Agent': 'myUserAgent'}

counter = 0
thread_count = 2
requests_per_thread = 10



@timer
def thread_func(url, header):
    global counter
    for i in range(requests_per_thread):
        response = limited_request(url, header)
        print(response)


t_start = time.time()
threads = [threading.Thread(target=thread_func, args=[URL, HEADER]) for _ in range(thread_count)]
for thread in threads:
    thread.start()

finished = False
while not finished:
    finished = True
    for thread in threads:
        if thread.is_alive():
            finished = False

t = time.time() - t_start

print(f'requests per second: {(thread_count * requests_per_thread) / t}')
