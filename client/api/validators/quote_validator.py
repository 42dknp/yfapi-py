"""
Module: QuoteValidator

Copyright 2023 Dominic Kneup.
Licensed under the MIT License; you can find the LICENSE file in the project's root folder.
"""
from client.exceptions.APIClientExceptions import ValidatorException


class QuoteValidator:
    """
    Class QuoteValidator
    Attributes:
        required_properties: list, required Properties to check
        multi_dimensional_properties: list, required multi-dimensionalProperties to check
    """
    required_properties = [
        'currency',
        'symbol',
        'fullExchangeName',
        'firstTradeDateMilliseconds',
        'exchangeTimezoneName',
        'regularMarketPrice',
        'priceHint',
    ]

    multi_dimensional_properties = [
        'fiftyTwoWeekLowChange',
        'fiftyTwoWeekHighChangePercent',
        'regularMarketDayRange',
        'regularMarketDayHigh',
        'fiftyTwoWeekHigh',
        'regularMarketPreviousClose',
        'fiftyTwoWeekHighChange',
        'marketCap',
        'regularMarketChange',
        'fiftyTwoWeekRange',
        'regularMarketVolume',
        'regularMarketDayLow',
    ]

    @staticmethod
    def validate_results(data) -> None:
        """
        Validate Quote Properties exists
        @param data: data to validate
        @return: None
        """
        for data_property in QuoteValidator.required_properties:
            if data_property not in data['quoteResponse']['result'][0]:
                raise ValidatorException('Missing ' + data_property + ' property')

        for data_property in QuoteValidator.multi_dimensional_properties:
            if data_property not in data['quoteResponse']['result'][0] or \
                    'raw' not in data['quoteResponse']['result'][0][data_property] or \
                    'fmt' not in data['quoteResponse']['result'][0][data_property]:
                raise ValidatorException('Invalid sub-properties for ' + data_property)
