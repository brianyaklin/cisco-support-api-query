"""A module for querying Cisco's EoX Support API end-point

This module provides an interface for querying Cisco's EoX
Support API.

    Typical usage example:

    pids = ['WS-C3750X-48PF-S','C3KX-PWR-1100WAC']
    eox = ApiEox("my_auth_token")
    eox.query_by_pid(pids)
    print(eox.records)
"""

from typing import List
from typing import Dict
import time
import requests


class ApiEox():
    """Cisco EoX API handler

    Provides a handler for interacting with the Cisco EoX Support API
    """

    def __init__(self, auth_token: str, mime_type: str = 'application/json') -> None:
        """Initializes the class

        Initilizes the class and sets the authorization token and MIME type
        to be used within the URL headers.

        Args:
            auth_token: A string represting the authorization token
            mime_type:
                A string representing the content-type for the response data

        Attributes:
            records: A list of dictionaries representing EOXRecord
                responses from the Cisco Support Bug API.
        """
        self.url_headers = {
            'Accept': mime_type,
            'Authorization': auth_token,
        }
        self.items = []
        self.records = []

    def __send_query(self, url: str,) -> Dict:
        """Send query to a specific URL

        Sends a requests get to the provided URL. The self.url_headers
        attribute will be used in the request.

        Args:
            url: A string representing the URL to query

        Returns:
            A dict representing the JSON response from the requests library

        Raises:
            requests.exceptions.HTTPError: An HTTP errors occured when querying
                the API. Usually a 4xx client error or 5xx server error
                response
        """
        req = requests.get(
            url,
            headers=self.url_headers
        )
        req.raise_for_status()
        return req.json()

    def query_by_pid(self, pids: List[str]) -> None:
        """Query EoX API end-point by PID

        Queries the EoX API end-point by prodict ID (PID). This takes a list
        of PID's, deduplicates the list as well as filters out some common
        blacklisted PID's that are often discovered by various data gathering
        sources (ex. Netmiko and textfsm parsing 'show inventory').

        Args:
            pids: A list of strings, each item representing a PID to query

        Raises:
            requests.exceptions.HTTPError: An HTTP errors occured when querying
                the API. Usually a 4xx client error or 5xx server error
                response
        """
        BLACK_LIST = ['', 'n/a', 'b', 'p', '^mf', 'unknown',
                      'unspecified', 'x']
        MAX_ITEMS = 20

        self.items = list({pid for pid in pids if pid.lower() not in BLACK_LIST})

        API_URL = 'https://api.cisco.com/supporttools/eox/rest/5/EOXByProductID/{}/{}'

        start_index = 0
        end_index = MAX_ITEMS
        while start_index <= len(self.items) - 1:
            page_index = 1
            pagination = True
            while pagination:
                url = API_URL.format(
                    page_index,
                    (',').join(self.items[start_index:end_index])
                )
                resp = self.__send_query(url)

                if resp.get('EOXRecord'):
                    self.records = self.records + resp['EOXRecord']

                if page_index >= resp['PaginationResponseRecord']['LastIndex']:
                    pagination = False
                else:
                    page_index += 1

                # Play nice with Cisco API's and rate limit your queries
                time.sleep(0.5)

            start_index = end_index
            end_index += MAX_ITEMS
