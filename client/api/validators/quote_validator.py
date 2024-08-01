"""
Module: QuoteValidator

Copyright 2023 Dominic Kneup.
Licensed under the MIT License; you can find the LICENSE file in the project's root folder.
"""
from client.exceptions.APIClientExceptions import ValidatorException


class QuoteValidator:
    """
    Validates the presence of required properties in quote data.

    Attributes:
        required_properties (list[str]): List of required properties to check in the quote data.
        multi_dimensional_properties (list[str]): List of required multi-dimensional properties
        to check in the quote data.
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
        Validates that all required properties and multi-dimensional properties exist
        in the given data.

        Args:
            data (dict): The data to validate.

        Raises:
            ValidatorException: If any required property or multi-dimensional property
            is missing or invalid.
        """
        if 'quoteResponse' not in data or 'result' not in data['quoteResponse'] or \
                not data['quoteResponse']['result']:
            raise ValidatorException('Missing quoteResponse property')

        quote = data['quoteResponse']['result'][0]

        # Check each required property in the quote data
        for data_property in QuoteValidator.required_properties:
            if data_property not in quote:
                raise ValidatorException(f'Missing {data_property} property')

        # Check each multi-dimensional property and ensure 'raw' and 'fmt' keys are present
        for data_property in QuoteValidator.multi_dimensional_properties:
            if data_property not in quote or \
                    'raw' not in quote[data_property] or \
                    'fmt' not in quote[data_property]:
                raise ValidatorException(f'Invalid sub-properties for {data_property}')
