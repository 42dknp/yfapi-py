"""
Module: SimilarSecuritiesValidator

Copyright 2023 Dominic Kneup.
Licensed under the MIT License; you can find the LICENSE file in the project's root folder.
"""
from typing import Dict, List
from client.exceptions.APIClientExceptions import ValidatorException


class SimilarSecuritiesValidator:
    """
    Validates the presence of required properties in similar securities data.

    Attributes:
        required_properties (list[str]): List of required properties to check in the
        similar securities data.
        indicator_properties (Dict[str, List[str]]): Dictionary of required indicator
        properties and their sub-properties.
    """

    # Required properties to check in the similar securities data
    required_properties: list = [
        'symbol',
        'recommendedSymbols'
    ]

    # Required indicator properties to check within 'recommendedSymbols'
    indicator_properties: Dict[str, List[str]] = {
        'recommendedSymbols': [
            'symbol',
            'score'
        ]
    }

    @classmethod
    def validate_results(cls, data) -> None:
        """
        Validates that all required properties and indicator sub-properties exist in the given data.

        Args:
            data (dict): The data to validate.

        Raises:
            ValidatorException: If any required property or sub-property is missing or invalid.
        """
        if 'finance' not in data:
            raise ValidatorException("Invalid similar securities data. Missing 'finance' field.")
        if 'result' not in data['finance']:
            raise ValidatorException(
                "Invalid similar securities data. Missing 'result' field in 'finance'."
            )
        if not data['finance']['result']:
            raise ValidatorException("Invalid similar securities data. 'result' field is empty.")

        # Check each required property in the similar securities data
        for prop in cls.required_properties:
            if prop not in data['finance']['result'][0]:
                raise ValidatorException(f'Missing {prop} property')

        # Check the 'recommendedSymbols' property
        recommended_symbols = data['finance']['result'][0]['recommendedSymbols']

        # Ensure 'recommendedSymbols' is a list
        if not isinstance(recommended_symbols, list):
            raise ValidatorException('Invalid recommendedSymbols format')

        # Check each sub-property within 'recommendedSymbols'
        for recommended_symbol in recommended_symbols:
            for sub_prop in cls.indicator_properties['recommendedSymbols']:
                if sub_prop not in recommended_symbol:
                    raise ValidatorException(f'Invalid sub-properties for {sub_prop}')
