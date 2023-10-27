"""
Module: Crumb

Copyright 2023 Dominic Kneup.
Licensed under the MIT License; you can find the LICENSE file in the project's root folder.
"""
from client.api_client import ApiClient
from client.api.validators.crumb_validator import CrumbValidator


class Crumb(ApiClient):
    """
    Class: Crumb
    Attributes:
        cookie_endpoint (str): The cookie endpoint for the crumb.
        crumb_endpoint (str): The crumb api Endpoint URL
    """
    # The cookie endpoint for the crumb.
    cookie_endpoint: str = 'https://fc.yahoo.com'

    # The crumb api Endpoint URL
    crumb_endpoint: str = 'https://query1.finance.yahoo.com/v1/test/getcrumb'

    def get_crumb(self) -> str:
        """
        Get Yahoo Finance Crumb
        @return: A new crumb for further use
        """

        # Get cookies into YahooFinanceAPI Instance for Crumb Request
        self.request_api(self.cookie_endpoint)

        # Get crumb
        crumb = self.request_api(self.crumb_endpoint)

        return CrumbValidator.validate_crumb(crumb)
