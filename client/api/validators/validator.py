"""
Module: Validator

Copyright 2023 Dominic Kneup.
Licensed under the MIT License; you can find the LICENSE file in the project's root folder.
"""
import re
import json
import os
import datetime
from client.exceptions.APIClientExceptions import ValidatorException


class Validator:
    """
    Class Validator
    Attributes:
        valid_intervals (list): Valid intervals for chart / time series data
    """
    # Valid intervals for chart / time series data
    ValidatorException = None
    valid_intervals = [
        "1d", "5d", "1wk", "1mo", "3mo", "6mo", "1y", "2y", "5y", "10y", "ytd", "max"
    ]

    @staticmethod
    def valid_url(url: str) -> bool:
        """
        Validates URL
        @param url: A url to validate
        @return: True if valid URL, throws Exception if not
        """
        if url and re.match(r'^(https?://[^/]+)(/.*)?$', url):
            return True
        raise ValidatorException("Invalid URL")

    @staticmethod
    def check_interval(interval: str) -> bool:
        """
        Check if interval is valid (based on attribute validIntervals)
        @param interval: interval to check
        @return: True if valid interval, throws Exception if not
        """
        if interval and interval in Validator.valid_intervals:
            return True
        raise ValidatorException("Invalid Interval")

    @staticmethod
    def validate_dates(start_date: datetime.datetime, end_date: datetime.datetime) -> bool:
        """
        Checks start_date and end_date is correct (valid date and start_date < end_date)
        @param start_date: period1 of api Call
        @param end_date: period2 of api Call
        @return: True if start_date and end_date exists and start_date > end_date,
        throws Exception if not
        """
        if start_date and end_date and start_date < end_date:
            return True
        raise ValidatorException('Invalid dates')

    @staticmethod
    def check_user_agent_file_exists(path: str) -> bool:
        """
        Checks that useragent.json file exists
        @param path: Path to file
        @return: True if file exists, throws Exception if not
        """
        if os.path.exists(path) or os.access(path, os.R_OK):
            return True
        raise ValidatorException(f'Failed to read the {path} file')

    @staticmethod
    def check_user_agent_file_empty_or_no_list(path: str) -> bool:
        """
        Checks that useragent.json file is not empty and a list
        @param path: Path to file useragent.json
        @return: True if file exists, and it is a list, throws Exception if not
        """
        try:
            with open(path, 'r', encoding="UTF-8") as file:
                user_agents = json.load(file)
                if not isinstance(user_agents, list) or not user_agents:
                    raise ValidatorException(f'No user agents found in {path}')
        except json.JSONDecodeError as exc:
            raise ValidatorException(f'Failed to decode {path}') from exc
        return False

    @staticmethod
    def check_response_error(data: str) -> None:
        """
        Checks if api response contains error message
        @param data: The raw api response
        @throws: ValidatorError
        @return: None
        """
        ex_message = "api response contains Error. Maybe your parameters are invalid"
        response_data = json.loads(data)

        if "chart" in response_data and "error" in response_data["chart"]:
            chart_error = response_data["chart"]["error"]
            if chart_error is not None:
                raise ValidatorException(ex_message)

        if "quoteResponse" in response_data and "result" in response_data["quoteResponse"]:
            result = response_data["quoteResponse"]["result"]
            if not result:
                raise ValidatorException(ex_message)

        if "finance" in response_data and "result" in response_data["finance"]:
            result = response_data["finance"]["result"]
            if not result:
                raise ValidatorException(ex_message)
