"""
Module: SimilarSecuritiesTransformer

Copyright 2023 Dominic Kneup.
Licensed under the MIT License; you can find the LICENSE file in the project's root folder.
"""
import json
from enum import Enum
from typing import Union, List
from client.api.transformers.transformer import Transformer
from client.api.validators.similar_securities_validator import SimilarSecuritiesValidator
from client.exceptions import APIClientExceptions


class OutputFormat(Enum):
    """Enum for output formats

    This enum defines the possible output formats for the similar securities data.
    The available formats are 'list' and 'raw'.
    """
    LIST = "list"
    RAW = "raw"


class SimilarSecuritiesTransformer(Transformer):
    """Class for transforming similar securities data API responses

    This class provides methods for transforming and validating similar securities data
    from API responses.
    """
    @staticmethod
    def _extract_symbols(finance_result: dict) -> List[str]:
        """Extracts similar securities symbols from the finance result

        This method extracts the similar securities symbols from the finance
        result and returns them as a list.
        Args:
            finance_result (dict): The finance result containing the similar securities data.
        Returns:
            List[str]: The list of similar securities symbols.
        """
        symbols = []
        for item in finance_result.get('result', []):
            for recommended_symbol in item.get('recommendedSymbols', []):
                symbol = recommended_symbol.get('symbol')
                if symbol:
                    symbols.append(symbol)
        return symbols

    @classmethod
    def data_transformation(cls, data: str) -> List[str]:
        """Validates and transforms similar securities data

        This method validates and transforms the similar securities data from the API response.

        Args:
            data (str): The raw JSON data from the API response.

        Returns:
            List[str]: The list of similar securities symbols.

        Raises:
            APIClientExceptions.TransformerException: If an error occurs during transformation.
        """
        try:
            data = json.loads(data)
        except json.JSONDecodeError as e:
            raise APIClientExceptions.JSONDecodeError(
                "API response contains error. Maybe your parameters are invalid"
            ) from e
        try:
            SimilarSecuritiesValidator.validate_results(data)
        except APIClientExceptions.ValidatorException as e:
            raise APIClientExceptions.TransformerException(str(e))
        finance_result = data.get('finance', {})
        return cls._extract_symbols(finance_result)

    @classmethod
    def output(cls, data: str, output_format: OutputFormat) -> Union[str, List[str]]:
        """
        Returns similar securities in the specified output format.

        Args:
            data (str): Raw JSON data from the API response.
            output_format (OutputFormat): Desired output format.

        Returns:
            Union[str, List[str]]: Similar securities data in the specified output format.
        """
        try:
            if output_format == OutputFormat.LIST:
                return cls.data_transformation(data)
            return data
        except (APIClientExceptions.JSONDecodeError, APIClientExceptions.TransformerException) as e:
            raise APIClientExceptions.TransformerException(str(e))
