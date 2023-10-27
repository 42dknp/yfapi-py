"""
Module: SimilarSecuritiesTransformer

Copyright 2023 Dominic Kneup.
Licensed under the MIT License; you can find the LICENSE file in the project's root folder.
"""
from typing import Union
from client.api.transformers.transformer import Transformer
from client.api.validators.similar_securities_validator import SimilarSecuritiesValidator
from client.exceptions.APIClientExceptions import TransformerException


class SimilarSecuritiesTransformer:
    """
    Class SimilarSecuritiesTransformer
    """
    OUTPUT_LIST = "list"
    OUTPUT_RAW = "raw"

    @staticmethod
    def data_transformation(data: str) -> list:
        """
        Validates and Transforms Similar Securities data
        @param data: The raw json from api as input
        @throws: Exception
        @return: A list with Similar Securities data
        """
        try:
            # Load JSON data
            result = dict(Transformer.decode_json_response(data))
            # Validate Object
            SimilarSecuritiesValidator.validate_results(result)

            symbols = []

            finance_result = result.get('finance', {}).get('result', [])
            for item in finance_result:
                recommended_symbols = item.get('recommendedSymbols', [])
                for recommended_symbol in recommended_symbols:
                    symbol = recommended_symbol.get('symbol')
                    if symbol:
                        symbols.append(symbol)

            return symbols
        except Exception as e:
            raise TransformerException("Error transforming Similar Securities data: " + str(e)) \
                from e

    @classmethod
    def output(cls, data: str, output: str) -> Union[str, list]:
        """
        Takes raw json from api response and converts / formats it
        @param data: raw json as input
        @param output: either raw, list or dict
        @return: Return converted and formatted data
        """
        if output == cls.OUTPUT_LIST:
            return cls.data_transformation(data)
        if output == cls.OUTPUT_RAW:
            return data
        raise TransformerException("Output format invalid")
