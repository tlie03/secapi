from ratelimiter import RateLimiter
import requests

REQUEST_COUNT = 10
PERIOD = 1


@RateLimiter(max_calls=REQUEST_COUNT, period=PERIOD)
def limited_request(url, header=None):
    return requests.get(url=url, headers=header)
