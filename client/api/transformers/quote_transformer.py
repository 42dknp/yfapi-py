"""
Module: QuoteTransformer

Copyright 2023 Dominic Kneup.
Licensed under the MIT License; you can find the LICENSE file in the project's root folder.
"""
from enum import Enum
from typing import Dict, List, Union
from client.api.transformers.transformer import Transformer
from client.api.validators.quote_validator import QuoteValidator
from client.exceptions import APIClientExceptions


class OutputFormat(Enum):
    """Enum for output formats

    This enum defines the possible output formats for the quote data.
    The available formats are 'list' and 'raw'.
    """
    DICT = "dict"
    RAW = "raw"


class QuoteTransformer:
    """
    Quote Transformer Class
    """
    def __init__(self):
        self.transformer = Transformer()
        self.validator = QuoteValidator()

    def _data_transformation(self, result: str, data_type: str) -> Dict:
        """
        Validates and transforms quote data.

        Args:
            result (str): Raw JSON from API.
            data_type (str): Type of data (e.g., "quote").

        Returns:
            Dict: Transformed quote data.

        Raises:
            APIClientExceptions.TransformerException: If transformation fails.
        """
        try:
            data = self.transformer.json_to_list(result)
            self.validator.validate_results(data)
            return self.transformer.flatten_dict(data[data_type]["result"][0])
        except (KeyError, ValueError) as e:
            raise APIClientExceptions.TransformerException(
                "Error transforming quote data due to missing keys or value errors."
            ) from e
        except Exception as e:
            raise APIClientExceptions.TransformerException(
                "Error transforming quote data due to an unexpected error."
            ) from e

    @staticmethod
    def transform_fields(fields: List[str], allowed_fields: List[str]) -> str:
        """
        Transform allowed fields into a comma-separated string.

        Args:
            fields (List[str]): Input fields to transform.
            allowed_fields (List[str]): Allowed fields.

        Returns:
            str: Comma-separated string of valid fields for API requests.
        """
        valid_fields = [field for field in fields if field in allowed_fields]
        return ",".join(valid_fields)

    def _return_quote_dict(self, data: str) -> Dict:
        """
        Converts and returns quote data as a dictionary.

        Args:
            data (str): Raw JSON data.

        Returns:
            Dict: Converted quote data.
        """
        return self._data_transformation(data, "quoteResponse")

    @classmethod
    def output(cls, data: str, output: str) -> Union[Dict, str]:
        """
        Returns quote data in the specified output format.

        Args:
            data (str): Raw JSON data.
            output (str): Desired output format (OutputFormat).

        Returns:
            Union[Dict, str]: Converted and formatted data.

        Raises:
            APIClientExceptions.TransformerException: If output format is invalid.
        """
        instance = cls()
        if output == OutputFormat.DICT.value:
            return instance._return_quote_dict(data)
        if output == OutputFormat.RAW.value:
            return data
        raise APIClientExceptions.TransformerException("Output format invalid")
