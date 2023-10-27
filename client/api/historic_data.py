"""
Module: HistoricData

Copyright 2023 Dominic Kneup.
Licensed under the MIT License; you can find the LICENSE file in the project's root folder.
"""
from datetime import datetime, timedelta
from typing import Union, Optional, List, Any, Dict
from client.api_client import ApiClient
from client.api.crumb import Crumb
from client.api.validators.validator import Validator
from client.api.transformers.historic_data_transformer import HistoricDataTransformer
from client.exceptions.APIClientExceptions import ValidatorException


class HistoricData(ApiClient):
    """
    Class HistoricData
    Attributes:
        endpoint (str): api Endpoint URL (optional)
        interval (str):  Define interval (optional)
        output (str): Setup Default Output Format (optional)
        crumb (str): Define existing Crumb (optional)
    """
    # api Endpoint URL
    endpoint: str = "https://query1.finance.yahoo.com/v8/finance/chart/"

    # Define interval
    interval: str = "1d"

    # Setup Default Output Format
    output: str = "dict"

    # Define existing Crumb
    crumb: Optional[str] = None

    def get_historic_data(self, symbol: str, start_date: datetime,
                          end_date: datetime) -> Union[str, List[Dict[Any, Any]]]:
        """
        Get Historic Date for a specified period
        @param symbol: The Security / Stock symbol
        @param start_date: Specify the start date
        @param end_date: Specify the end date
        @return: A list / dict of similar securities or raw json api response
        """

        if (Validator.check_interval(self.interval)
                and Validator.validate_dates(start_date, end_date)):

            url = self.endpoint + symbol
            if not self.crumb:
                get_crumb = Crumb()
                self.crumb = get_crumb.get_crumb()
            params = {
                'period1': int(start_date.timestamp()),
                'period2': int(end_date.timestamp()),
                'interval': self.interval,
                'crumb': self.crumb
            }
            response = self.request_api(url, params)

            # Check response for errors
            Validator.check_response_error(response)

            return HistoricDataTransformer.output(response, self.output)
        raise ValidatorException("Cannot validate input")

    def get_historic_data_ytd(self, symbol: str) -> Union[str, List[Dict[Any, Any]]]:
        """
        Get Historic data for this year (Jan 1st - today)
        @param symbol: The Security / Stock symbol
        @return: A list / dict of similar securities or raw json api response
        """
        return self.get_historic_data(
            symbol,
            datetime(datetime.now().year, 1, 1),
            datetime.today()
        )

    def get_historic_data_last_year(self, symbol: str) -> Union[str, List[dict]]:
        """
        Get Historic data for last year
        @param symbol: The Security / Stock symbol
        @return: A list / dict of similar securities or raw json api response
        """
        return self.get_historic_data(
            symbol,
            datetime(datetime.now().year - 1, 1, 1),
            datetime(datetime.now().year - 1, 12, 31)
        )

    def get_historic_data_last_30_days(self, symbol: str) -> Union[str, List[dict]]:
        """
        Get Historic data for last 30 days
        @param symbol: The Security / Stock symbol
        @return: A list / dict of similar securities or raw json api response
        """
        today = datetime.today()
        return self.get_historic_data(
            symbol,
            datetime(today.year, today.month - 1, 1),
            datetime(today.year, today.month - 1, today.day)
        )

    def get_historic_data_last_month(self, symbol: str) -> Union[str, List[dict]]:
        """
        Get Historic data for the last month (previous calendar month)
        @param symbol: The Security / Stock symbol
        @return: A list / dict of similar securities or raw JSON api response
        """
        today = datetime.today()
        last_day_of_last_month = today.replace(day=1) - timedelta(days=1)
        first_day_of_last_month = last_day_of_last_month.replace(day=1)

        return self.get_historic_data(
            symbol,
            first_day_of_last_month,
            last_day_of_last_month
        )

    def get_historic_data_last_week(self, symbol: str) -> Union[str, List[dict]]:
        """
        Get Historic data for last week (monday to friday last week)
        @param symbol: The Security / Stock symbol
        @return: A list / dict of similar securities or raw json api response
        """
        today = datetime.today()
        monday = today - timedelta(days=today.weekday())
        sunday = monday + timedelta(days=6)
        return self.get_historic_data(
            symbol,
            monday,
            sunday
        )
