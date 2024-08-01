"""
Module: HistoricData

Copyright 2023 Dominic Kneup.
Licensed under the MIT License; you can find the LICENSE file in the project's root folder.
"""
import logging
from datetime import datetime, timedelta
from typing import Union, Optional, List, Any, Dict
from client.api_client import ApiClient
from client.api.crumb import Crumb
from client.api.validators.validator import Validator
from client.api.transformers.historic_data_transformer import HistoricDataTransformer
from client.exceptions.APIClientExceptions import ValidatorException
from client.api.config import settings

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class HistoricData(ApiClient):
    """
    Class HistoricData
    Attributes:
        endpoint (str): API Endpoint URL
        interval (str): Define interval
        output (str): Setup Default Output Format
        yf_crumb (str): Define existing Crumb
    """
    def __init__(
            self,
            endpoint: str = settings.historic_data_api_endpoint,
            interval: str = settings.historic_data_interval,
            output: str = settings.historic_data_output):
        super().__init__()
        self.endpoint = endpoint
        self.interval = interval
        self.output = output
        self.yf_crumb: Optional[str] = None

    def get_historic_data(
            self,
            symbol: str,
            start_date: datetime,
            end_date: datetime) -> Union[str, List[Dict[Any, Any]]]:
        """
        Get Historic Data for a specified period
        @param symbol: The Security / Stock symbol
        @param start_date: Specify the start date
        @param end_date: Specify the end date
        @return: A list / dict of similar securities or raw JSON API response
        """
        logger.info("Fetching historic data for symbol: %s from %s to %s",
                    symbol, start_date, end_date)

        if Validator.check_interval(self.interval) and \
                Validator.validate_dates(start_date, end_date):
            url = self.endpoint + symbol

            if not self.yf_crumb:
                logger.info("Crumb is empty, fetching new crumb")
                get_crumb = Crumb()
                self.yf_crumb = get_crumb.get_crumb()

            params = {
                'period1': int(start_date.timestamp()),
                'period2': int(end_date.timestamp()),
                'interval': self.interval,
                'crumb': self.yf_crumb
            }

            try:
                response = self.request_api(url, params)
                Validator.check_response_error(response)
                return HistoricDataTransformer.output(response, self.output)

            except Exception as e:
                logger.error("Error fetching historic data for symbol %s: %s", symbol, e)
                raise

        raise ValidatorException("Cannot validate input")

    def get_historic_data_ytd(self, symbol: str) -> Union[str, List[Dict[Any, Any]]]:
        """
        Get Historic data for this year (Jan 1st - today)
        @param symbol: The Security / Stock symbol
        @return: A list / dict of similar securities or raw JSON API response
        """
        return self._get_historic_data_for_period(
            symbol,
            datetime(datetime.now().year, 1, 1),
            datetime.today()
        )

    def get_historic_data_last_year(self, symbol: str) -> Union[str, List[dict]]:
        """
        Get Historic data for last year
        @param symbol: The Security / Stock symbol
        @return: A list / dict of similar securities or raw JSON API response
        """
        return self._get_historic_data_for_period(
            symbol,
            datetime(datetime.now().year - 1, 1, 1),
            datetime(datetime.now().year - 1, 12, 31))

    def get_historic_data_last_30_days(self, symbol: str) -> Union[str, List[dict]]:
        """
        Get Historic data for last 30 days
        @param symbol: The Security / Stock symbol
        @return: A list / dict of similar securities or raw JSON API response
        """
        today = datetime.today()
        return self._get_historic_data_for_period(symbol, today - timedelta(days=30), today)

    def get_historic_data_last_month(self, symbol: str) -> Union[str, List[dict]]:
        """
        Get Historic data for the last month (previous calendar month)
        @param symbol: The Security / Stock symbol
        @return: A list / dict of similar securities or raw JSON API response
        """
        today = datetime.today()
        last_day_of_last_month = today.replace(day=1) - timedelta(days=1)
        first_day_of_last_month = last_day_of_last_month.replace(day=1)
        return self._get_historic_data_for_period(
            symbol,
            first_day_of_last_month,
            last_day_of_last_month
        )

    def get_historic_data_last_week(self, symbol: str) -> Union[str, List[dict]]:
        """
        Get Historic data for last week (Monday to Sunday last week)
        @param symbol: The Security / Stock symbol
        @return: A list / dict of similar securities or raw JSON API response
        """
        today = datetime.today()
        monday = today - timedelta(days=today.weekday() + 7)
        sunday = monday + timedelta(days=6)
        return self._get_historic_data_for_period(symbol, monday, sunday)

    def _get_historic_data_for_period(
            self,
            symbol: str,
            start_date: datetime,
            end_date: datetime) -> Union[str, List[Dict[Any, Any]]]:
        """
        Helper method to get historic data for a specified period
        @param symbol: The Security / Stock symbol
        @param start_date: Specify the start date
        @param end_date: Specify the end date
        @return: A list / dict of similar securities or raw JSON API response
        """
        return self.get_historic_data(symbol, start_date, end_date)
