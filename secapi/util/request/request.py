import requests
from ratelimit import limits, sleep_and_retry

SEC_REQUEST_COUNT = 10
SEC_PERIOD = 1
SEC_HEADER = {'User-Agent': "myUserAgent"}


class Request:

    @staticmethod
    @sleep_and_retry
    @limits(calls=SEC_REQUEST_COUNT, period=SEC_PERIOD)
    def sec_request(url, header=None):
        if header is None:
            header = SEC_HEADER
        return requests.get(url=url, headers=header)
