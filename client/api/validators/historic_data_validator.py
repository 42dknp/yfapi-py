"""
Module: HistoricDataValidator

Copyright 2023 Dominic Kneup.
Licensed under the MIT License; you can find the LICENSE file in the project's root folder.
"""
from client.exceptions.APIClientExceptions import ValidatorException


class HistoricDataValidator:
    """
    Class HistoricDataValidator
    Attributes:
        required_properties (list): required Properties to check
        indicator_properties (dict): required indicator Properties to check
    """
    # required Properties to check
    required_properties: list = [
        'currency',
        'symbol',
        'exchangeName',
        'instrumentType',
        'firstTradeDate',
        'timezone',
        'exchangeTimezoneName',
        'regularMarketPrice',
        'chartPreviousClose',
        'priceHint'
    ]
    # required indicator Properties to check
    indicator_properties: dict = {
        'quote': ['low', 'high', 'volume', 'close', 'open'],
        'adjclose': ['adjclose']
    }

    @classmethod
    def validate_results(cls, data: dict) -> None:
        """
        Validate Historic data Properties exists
        @param data: data to validate
        @return: None
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
                        raise ValidatorException('Invalid sub-properties for ' + sub_data_property)
