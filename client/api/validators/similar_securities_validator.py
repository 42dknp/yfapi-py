"""
Module: SimilarSecuritiesValidator

Copyright 2023 Dominic Kneup.
Licensed under the MIT License; you can find the LICENSE file in the project's root folder.
"""
from typing import Dict, List
from client.exceptions.APIClientExceptions import ValidatorException


class SimilarSecuritiesValidator:
    """
    Class SimilarSecuritiesValidator
    Attributes:
        required_properties: list, Required Properties to check
        indicator_properties: list, Required Indicator Properties to check
    """

    # Required Properties to check
    required_properties: list = [
        'symbol',
        'recommendedSymbols'
    ]

    # Required Indicator Properties to check
    indicator_properties: Dict[str, List[str]] = {
        'recommendedSymbols': [
            'symbol',
            'score'
        ]
    }

    @classmethod
    def validate_results(cls, data) -> None:
        """
        Check required properties
        @param data: A list with Similar Securities data
        @return: None
        """
        for prop in cls.required_properties:
            if prop not in data['finance']['result'][0]:
                raise ValidatorException('Missing ' + prop + ' property')

        # Check recommendedSymbols property
        recommended_symbols = data['finance']['result'][0]['recommendedSymbols']
        if not isinstance(recommended_symbols, list):
            raise ValidatorException('Invalid recommendedSymbols format')
        for recommended_symbol in recommended_symbols:
            for sub_prop in cls.indicator_properties['recommendedSymbols']:
                if sub_prop not in recommended_symbol:
                    raise ValidatorException('Invalid sub-properties for ' + sub_prop)
