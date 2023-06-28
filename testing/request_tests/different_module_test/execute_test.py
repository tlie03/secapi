"""
This test is based on the assumption that the ratelimit does not work when the requests are made from different modules.
"""
from module1.requester1 import execute1
from module2.requester2 import execute2


if __name__ == "__main__":
    threads = []
    threads += execute1()
    threads += execute2()
    for thread in threads:
        thread.join()