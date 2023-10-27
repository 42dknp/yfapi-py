"""
Module: ApiClient

Copyright 2023 Dominic Kneup.
Licensed under the MIT License; you can find the LICENSE file in the project's root folder.
"""
import os
import json
import random
from typing import Dict, Optional, Any
import requests
from client.api.validators.validator import Validator
from client.exceptions.APIClientExceptions import BaseAPIClientException, APIClientException


class ApiClient:
    """
    Class APIClient
    """

    def __init__(self):
        """
        Setup api client
        @var self.session: Stores Session Cookies
        """
        self.session = requests.Session()  # Create a session to persist cookies

    def request_api(self, url: str, params: Optional[Any] = None,
                    headers: Optional[Dict[str, str]] = None) -> str:
        """
        Send GET request with url to endpoint and return answer
        @param url: The URL for the api request.
        @param params: The parameters for the api request.
        @param headers:The headers for the api request (can be specified manually)
        @return: The response from the api as a string.
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
                # response.raise_for_status()  # Raise an exception for HTTP errors

                return response.text

            except requests.exceptions.RequestException as e:

                raise APIClientException(f'An error occurred: {str(e)} from e') from e
        else:
            return "An error accured"

    @staticmethod
    def get_random_user_agent() -> str:
        """
        Get a random User Agent from useragents.json file
        @return: Returns a random User Agent string
        """
        try:
            file_path = os.path.join(os.path.dirname(__file__), 'data/useragents.json')

            # Check if the file exists and is readable
            if not os.path.exists(file_path) or not os.access(file_path, os.R_OK):
                raise APIClientException('Failed to read useragents.json file')

            with open(file_path, encoding='utf-8') as file:
                user_agents_json = file.read()

            # Check if there was an error reading the file
            if not user_agents_json:
                raise APIClientException('Failed to read useragents.json file')

            user_agents = json.loads(user_agents_json)

            # Check if JSON decoding was successful and if user_agents is a list
            if not isinstance(user_agents, list):
                raise APIClientException('Failed to decode useragents.json')

            # Check if the list of user agents is empty
            if not user_agents:
                raise APIClientException('No user agents found in useragents.json')

        except Exception as e:
            raise BaseAPIClientException(f'An error occurred: {str(e)} from e') from e

        # Return a random user agent from the list
        return random.choice(user_agents)
