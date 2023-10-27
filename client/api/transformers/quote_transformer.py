"""
Module: QuoteTransformer

Copyright 2023 Dominic Kneup.
Licensed under the MIT License; you can find the LICENSE file in the project's root folder.
"""
from client.api.transformers.transformer import Transformer
from client.api.validators.quote_validator import QuoteValidator
from client.exceptions.APIClientExceptions import TransformerException


class QuoteTransformer:
    """
    Class QuoteTransformer
    """
    OUTPUT_DICT = "dict"
    OUTPUT_RAW = "raw"

    @staticmethod
    def data_transformation(result: str, data_type: str) -> dict:
        """
        Validates and Transforms Quote data
        @param result: string, The raw json from api as input
        @param data_type: string, api type (e.g. quote)
        @return: dict, A list with Quote data
        """
        try:
            data = dict(Transformer.decode_json_response(result))
            QuoteValidator.validate_results(data)
            return Transformer.flatten_data(data[data_type]["result"][0])
        except Exception as e:
            raise TransformerException("Error transform Quote Date.") from e

    @staticmethod
    def transform_fields(fields: list, allowed_fields: list) -> str:
        """
        Transform allowed Fields
        @param fields: Input Fields
        @param allowed_fields: Allowed Fields input
        @return: a string with all fields (for use in api request)
        """
        valid_fields = [field for field in fields if field in allowed_fields]

        return ','.join(valid_fields)

    @staticmethod
    def return_quote_dict(data: str) -> dict:
        """
        Converts and returns Quote data as Dictionary
        @param data: raw json data as input
        @return: converted Quote data as Output
        """
        return QuoteTransformer.data_transformation(data, "quoteResponse")

    @classmethod
    def output(cls, data: str, output: str):
        """
        Return Quote in specified Output Format
        @param data: raw json as input
        @param output: either raw, list or dict
        @return: Return converted and formatted data
        """
        if output == cls.OUTPUT_DICT:
            return cls.return_quote_dict(data)
        if output == cls.OUTPUT_RAW:
            return data
        raise TransformerException("Output Format invalid")
