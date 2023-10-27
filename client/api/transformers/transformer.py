"""
Module: Transformer

Copyright 2023 Dominic Kneup.
Licensed under the MIT License; you can find the LICENSE file in the project's root folder.
"""
import json
from client.exceptions.APIClientExceptions import TransformerException


class Transformer:
    """
    Class Transformer
    """
    @staticmethod
    def decode_json_response(response) -> list:
        """
        Converts json string into a list
        @param response: raw json string as input
        @return: returns a list
        """
        try:
            response_data = json.loads(response)
            if not response_data:
                raise TransformerException('Invalid JSON')

            return response_data
        except Exception as e:
            raise TransformerException("Expecting value: line 1 column 1 (char 0)") from e

    @staticmethod
    def flatten_data(data) -> dict:
        """
        Flattens Multi-dimensional dict into a 1-dimensional one
        @param data: Multi-dimensional dict
        @return: Returns a "flat" Dictionary
        """
        converted = {}
        for key, value in data.items():
            if isinstance(value, dict) and 'raw' in value:
                converted[key] = value['raw']
            elif isinstance(value, str):
                converted[key] = value

        return converted
