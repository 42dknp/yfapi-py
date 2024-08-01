"""
Module: HistoricDataValidator

Copyright 2023 Dominic Kneup.
Licensed under the MIT License; you can find the LICENSE file in the project's root folder.
"""
from client.exceptions.APIClientExceptions import ValidatorException


class HistoricDataValidator:
    """
    Validates the presence of required properties in historic data.

    Attributes:
        required_properties (list[str]): List of required properties to check in the 'meta' section.
        indicator_properties (dict[str, list[str]]): Dictionary of required indicator properties
        and their sub-properties.
    """
    required_properties: list[str] = [
        'currency', 'symbol', 'exchangeName', 'instrumentType', 'firstTradeDate',
        'timezone', 'exchangeTimezoneName', 'regularMarketPrice', 'chartPreviousClose', 'priceHint'
    ]

    indicator_properties: dict[str, list[str]] = {
        'quote': ['low', 'high', 'volume', 'close', 'open'],
        'adjclose': ['adjclose']
    }

    @classmethod
    def validate_results(cls, data: dict) -> None:
        """
        Validates that all required properties and indicator sub-properties exist in the given data.

        Args:
            data (dict): The data to validate.

        Raises:
            ValidatorException: If any required property or sub-property is missing.
        """
        for data_property in cls.required_properties:
            if not data['chart']['result'][0]['meta'].get(data_property):
                raise ValidatorException('Missing ' + data_property + ' property')

            for data_property, sub_properties in cls.indicator_properties.items():
                if not data['chart']['result'][0]['indicators'].get(data_property):
                    raise ValidatorException('Missing ' + data_property + ' property')

                if isinstance(sub_properties, list):
                    for sub_data_property in sub_properties:
                        if not (data['chart']['result'][0]['indicators'][data_property][0]
                                .get(sub_data_property)):
                            raise ValidatorException(
                                'Invalid sub-properties for ' + sub_data_property
                            )
