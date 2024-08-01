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
    Validates various aspects of input data such as URLs, intervals, dates, and file existence.

    Attributes:
        valid_intervals (list[str]): Valid intervals for chart/time series data.
    """

    # Valid intervals for chart/time series data
    valid_intervals: list[str] = [
        "1d", "5d", "1wk", "1mo", "3mo", "6mo", "1y", "2y", "5y", "10y", "ytd", "max"
    ]

    @staticmethod
    def valid_url(url: str) -> bool:
        """
        Validates if the given URL is well-formed.

        Args:
            url (str): A URL to validate.

        Returns:
            bool: True if valid URL, raises ValidatorException if not.
        """
        if url and re.match(r'^(https?://[^/]+)(/.*)?$', url):
            return True
        raise ValidatorException("Invalid URL")

    @staticmethod
    def check_interval(interval: str) -> bool:
        """
        Checks if the given interval is valid.

        Args:
            interval (str): Interval to check.

        Returns:
            bool: True if valid interval, raises ValidatorException if not.
        """
        if interval and interval in Validator.valid_intervals:
            return True
        raise ValidatorException("Invalid Interval")

    @staticmethod
    def validate_dates(start_date: datetime.datetime, end_date: datetime.datetime) -> bool:
        """
        Validates if the start_date is before the end_date.

        Args:
            start_date (datetime.datetime): Start date of the period.
            end_date (datetime.datetime): End date of the period.

        Returns:
            bool: True if start_date is before end_date, raises ValidatorException if not.
        """
        if not all([
                isinstance(start_date, datetime.datetime),
                isinstance(end_date, datetime.datetime)]):
            raise ValidatorException("Dates must be datetime objects")
        if start_date and end_date and start_date < end_date:
            return True
        raise ValidatorException('Invalid dates')

    @staticmethod
    def check_user_agent_file_exists(path: str) -> bool:
        """
        Checks if the useragent.json file exists and is readable.

        Args:
            path (str): Path to the file.

        Returns:
            bool: True if file exists and is readable, raises ValidatorException if not.
        """
        if os.path.exists(path) and os.access(path, os.R_OK):
            return True
        raise ValidatorException(f'Failed to read the {path} file')

    @staticmethod
    def check_user_agent_file_empty_or_no_list(path: str) -> bool:
        """
        Checks if the useragent.json file is not empty and contains a list.

        Args:
            path (str): Path to the useragent.json file.

        Returns:
            bool: True if file exists and contains a list, raises ValidatorException if not.
        """
        try:
            with open(path, 'r', encoding="UTF-8") as file:
                user_agents = json.load(file)
                if not isinstance(user_agents, list) or not user_agents:
                    raise ValidatorException(f'No user agents found in {path}')
        except json.JSONDecodeError as exc:
            raise ValidatorException(f'Failed to decode {path}') from exc
        return True

    @staticmethod
    def check_response_error(data: str) -> None:
        """
        Checks if the API response contains an error message.

        Args:
            data (str): The raw API response.

        Raises:
            ValidatorException: If the API response contains an error message.
        """
        ex_message = "API response contains error. Maybe your parameters are invalid"
        response_data = json.loads(data)

        # Check for errors in 'chart' section
        if "chart" in response_data and "error" in response_data["chart"]:
            chart_error = response_data["chart"]["error"]
            if chart_error is not None:
                raise ValidatorException(ex_message)

        # Check for empty 'result' in 'quoteResponse' section
        if "quoteResponse" in response_data and "result" in response_data["quoteResponse"]:
            result = response_data["quoteResponse"]["result"]
            if not result:
                raise ValidatorException(ex_message)

        # Check for empty 'result' in 'finance' section
        if "finance" in response_data and "result" in response_data["finance"]:
            result = response_data["finance"]["result"]
            if not result:
                raise ValidatorException(ex_message)
