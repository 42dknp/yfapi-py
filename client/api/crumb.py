"""
Module: Crumb

Copyright 2023 Dominic Kneup.
Licensed under the MIT License; you can find the LICENSE file in the project's root folder.
"""
import logging
from client.api_client import ApiClient
from client.api.validators.crumb_validator import CrumbValidator
from client.api.config import settings

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class Crumb(ApiClient):
    """
    Class: Crumb
    Attributes:
        cookie_endpoint (str): The cookie endpoint for the crumb.
        crumb_endpoint (str): The crumb API Endpoint URL.
    """
    def __init__(self,
                 cookie_endpoint: str = settings.crumb_cookie_endpoint,
                 crumb_endpoint: str = settings.crumb_api_endpoint):
        super().__init__()
        self.cookie_endpoint = cookie_endpoint
        self.crumb_endpoint = crumb_endpoint

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
