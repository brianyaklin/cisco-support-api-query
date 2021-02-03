"""A module for handling authentication Cisco Support API's

This module provides an interface for authenticating against the Cisco
Support API. You will require a valid client ID and secret. Once
authenticated, you can use the url_headers attribute for querying
the various support API's.

    Typical usage example:

    api = ApiLogin("my_client_key", "my_client_secret")
    SupportApiX(api.url_headers, additional_parameters)
    api.auth_still_valid()
    SupportApiY(api.url_headers, additional_parameters)

"""

import time
import requests


class ApiLogin():
    """Cisco Support API login handlers

    Provides base modules for the Cisco Support API
    such as login functionality and token renewal. This supports
    a grant type of client credentials.
    """

    def __init__(self, client_key: str, client_secret: str) -> None:
        """Initializes the class and logs in

        Logs into the Cisco Support API with the provided client
        ID and secret.

        Args:
            client_key: A string representing the API client key
            client_secret: A string representing the API client secret
        """
        self.client_key = client_key
        self.client_secret = client_secret
        self.login()

    def login(self) -> None:
        """Authenticates against the Cisco Support API

        Authenticates against the Cisco Support API using the
        initilized client ID and client secret.

        Attributes:
            auth_token: A string representing the URL header for authorization
                which will be used for subsequent API calls. The URL headers
                include a MIME type and an authorization header comprised of an
                access token and token type. An example:

                'Bearer 0123456789abcdef'
        """
        self.auth_token = None
        self.auth_start = time.time()
        SSO_URL = 'https://cloudsso.cisco.com/as/token.oauth2'

        params = {
            'grant_type': 'client_credentials',
            'client_id': self.client_key,
            'client_secret': self.client_secret,
        }

        req = requests.post(
            SSO_URL,
            params=params,
        )
        req.raise_for_status()

        self.auth_resp = req.json()

        self.auth_token = \
            f"{self.auth_resp['token_type']} {self.auth_resp['access_token']}"

    def auth_still_valid(self) -> None:
        """Determines if the auth token is still valid

        Compares the time the token was received with the current time
        and identifies if the delta is less than the expires in value.
        If the delta is greater, the token is no longer valid and a new
        token will be generated.
        """

        if (time.time() - self.auth_start) >= (self.auth_resp['expires_in']):
            # Login again, which will set a self.url_headers with a new token
            self.login()
