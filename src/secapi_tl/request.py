"""
This module provides the sec_request function which must be used
for all requests to the  sec.gov domain to ensure that the amount
of requests stays in the boundaries set by the sec.
"""
import requests
from faker import Faker
from ratelimit import limits, sleep_and_retry

SEC_REQUEST_COUNT = 1
SEC_PERIOD = 0.101
RETRIES = 10

SESSION = requests.Session()
FAKER = Faker()




def sec_request(url: str, header: dict = None) -> requests.Response:
    """
    This method performs the request to the sec.gov domain.
    It uses a rate limited method to make the requests.
    Thereby it ensures that the amount of requests stays in the boundaries set by the sec.

    :param url: the url to request
    :param header: the header to use for the request. If no User-Agent is set a random one will be generated.
    :return: the response (a response object from the requests module)
    :raises TooManyRequestsError: if the response status code is 429. This can be the case when the requested
    url is under too much load. Even though the amount of total requests is in the boundaries set by the sec.
    :raises ConnectionError: if the response status code is not 200 or 429 and the amount of retries is exceeded.
    """
    if header is None:
        header = {"User-Agent": create_user_agent()}
    elif "User-Agent" not in header:
        header["User-Agent"] = create_user_agent()

    retry = 0
    success = False
    while retry < RETRIES and not success:
        response = limit_request(url=url, header=header)

        if response.status_code != 200:
            if retry < RETRIES:
                retry += 1
                continue

            if response.status_code == 429:
                raise TooManyRequestsError(response.text)
            else:
                raise ConnectionError(f"invalid response status code {response.status_code}")

        else:
            success = True

    return response


@sleep_and_retry
@limits(calls=SEC_REQUEST_COUNT, period=SEC_PERIOD)
def limit_request(url: str, header: dict) -> requests.Response:
    return SESSION.get(url=url, headers=header)


def create_user_agent() -> str:
    """
    creates a random user agent string that will be accepted by the sec.
    A valid user agent string is required for all requests to the sec.gov domain.
    It contains a first name, last name and email address.
    """
    ua = f"{FAKER.first_name()} {FAKER.last_name()} {FAKER.email()}"
    return ua


class TooManyRequestsError(ConnectionError):
    """
    Error that is used for responses with status code 429.
    """

    def __init__(self, response_txt: str):
        self._response_txt = response_txt

    def __str__(self):
        return f"TooManyRequestsError. The following text was send with the response: {self._response_txt}"