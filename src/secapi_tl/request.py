"""
This module provides the sec_request function which must be used
for all requests to the  sec.gov domain to ensure that the amount
of requests stays in the boundaries set by the sec.
"""
import requests
from faker import Faker
from ratelimit import limits, sleep_and_retry
from threading import Semaphore

SEC_REQUEST_COUNT = 1
SEC_PERIOD = 0.101

SEMAPHORE = Semaphore(value=1)
SESSION = requests.Session()
FAKER = Faker()


@sleep_and_retry
@limits(calls=SEC_REQUEST_COUNT, period=SEC_PERIOD)
def sec_request(url: str):
    """
    This method performs the request to the sec.gov domain.
    It is rate limited to SEC_REQUEST_COUNT requests per SEC_PERIOD seconds.
    Thereby it ensures that the amount of requests stays in the boundaries set by the sec.

    :param url: the url to request
    :return: the response (a response object from the requests module)
    :raises ConnectionError: if the response status code is not 200
    """
    header = {"User-Agent": create_user_agent()}
    try:
        response = SESSION.get(url=url, headers=header)
    except Exception as err:
        raise err

    if response.status_code != 200:
        print(response.text)
        raise ConnectionError(f"invalid response status code {response.status_code}")
    return response


def create_user_agent() -> str:
    """
    creates a random user agent string that will be accepted by the sec.
    A valid user agent string is required for all requests to the sec.gov domain.
    It contains a first name, last name and email address.
    """
    ua = f"{FAKER.first_name()} {FAKER.last_name()} {FAKER.email()}"
    return ua
