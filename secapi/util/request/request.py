"""
This module provides the sec_request function which must be used
for all requests to the  sec.gov domain to ensure that the amount
of requests stays in the boundaries set by the sec.

The method was implemented as a static method of a class because
an implementation as a normal function caused some issues
by exceeding the request limits when used with threading.
These issues disappeared with the implementation as a static method.
"""

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
