"""
Module: ApiClient

Copyright 2023 Dominic Kneup.
Licensed under the MIT License; you can find the LICENSE file in the project's root folder.
"""
import os
import json
import random
from typing import Dict, Optional, Any
import logging
import requests
from client.api.validators.validator import Validator
from client.exceptions.APIClientExceptions import BaseAPIClientException, APIClientException

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class ApiClient:
    """
    Class APIClient
    """

    def __init__(self):
        """
        Setup API client
        """
        self.session = requests.Session()

    def request_api(self, url: str, params: Optional[Any] = None,
                    headers: Optional[Dict[str, str]] = None) -> str:
        """
        Send GET request with URL to endpoint and return answer
        @param url: The URL for the API request.
        @param params: The parameters for the API request.
        @param headers: The headers for the API request (can be specified manually)
        @return: The response from the API as a string.
        """
        if Validator.valid_url(url):
            try:
                if headers is None:
                    headers = {
                        'User-Agent': self.get_random_user_agent()
                    }
                response = self.session.get(
                    url,
                    headers=headers,
                    params=params
                )

                return response.text

            except requests.exceptions.RequestException as e:
                logger.error('An error occurred: %s', str(e))
                return response.text if response else None
        else:
            return "An error occurred"

    @staticmethod
    def get_random_user_agent() -> str:
        """
        Get a random User Agent from useragents.json file
        @return: Returns a random User Agent string
        """
        try:
            file_path = os.path.join(os.path.dirname(__file__), 'data/useragents.json')

            if not os.path.exists(file_path) or not os.access(file_path, os.R_OK):
                raise APIClientException('Failed to read useragents.json file')

            with open(file_path, encoding='utf-8') as file:
                user_agents_json = file.read()

            if not user_agents_json:
                raise APIClientException('Failed to read useragents.json file')

            user_agents = json.loads(user_agents_json)

            if not isinstance(user_agents, list):
                raise APIClientException('Failed to decode useragents.json')

            if not user_agents:
                raise APIClientException('No user agents found in useragents.json')

        except Exception as e:
            raise BaseAPIClientException(f'An error occurred: {str(e)}') from e

        return random.choice(user_agents)
