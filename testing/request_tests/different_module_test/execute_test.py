"""
This test is based on the assumption that the ratelimit does not work when the requests are made from different modules.
"""
from module1.requester1 import execute1
from module2.requester2 import execute2

import time


if __name__ == "__main__":
    threads = []
    threads += execute1()
    threads += execute2()
    start_time = time.time()
    for thread in threads:
        thread.join()
    end_time = time.time()
    total_time = end_time - start_time
    print(f"time: {total_time}")