"""
Module: HistoricDataTransformer

Copyright 2023 Dominic Kneup.
Licensed under the MIT License; you can find the LICENSE file in the project's root folder.
"""
from typing import Union, List, Dict, Any
from enum import Enum
from client.api.transformers.transformer import Transformer
from client.api.validators.historic_data_validator import HistoricDataValidator
from client.exceptions.APIClientExceptions import TransformerException


class OutputFormat(Enum):
    """Enum for output formats

    This enum defines the possible output formats for the historic data data.
    The available formats are 'dict' and 'raw'.
    """
    DICT = "dict"
    RAW = "raw"


class HistoricDataTransformer:
    """
    Class for transforming historic data API responses.
    """

    @staticmethod
    def transform_results(result: str, output: OutputFormat) -> List[Dict[str, Any]]:
        """
        Validates and transforms historic data from a raw JSON response.

        Args:
            result (str): Raw JSON from the API.
            output (OutputFormat): Desired output format.

        Returns:
            List[Dict[str, Any]]: A list of dictionaries containing historic data.

        Raises:
            TransformerException: If transformation fails.
        """
        try:
            data = dict(Transformer.json_to_list(result))
            HistoricDataValidator.validate_results(data)

            if 'chart' not in data or 'result' not in data['chart'] or not data['chart']['result']:
                raise TransformerException("Invalid data structure: missing 'chart' or 'result'")

            result_data = data['chart']['result'][0]
            if 'timestamp' not in result_data or 'indicators' not in result_data:
                raise TransformerException(
                    "Invalid data structure: missing 'timestamp' or 'indicators'"
                )

            timestamps = result_data['timestamp']
            quote_data = result_data['indicators']['quote'][0]
            adj_close_data = result_data['indicators']['adjclose'][0]['adjclose']

            processed_data = [
                HistoricDataTransformer.transform_single_data(
                    timestamps[i],
                    (quote_data['open'][i],
                     quote_data['low'][i],
                     quote_data['high'][i],
                     quote_data['close'][i],
                     adj_close_data[i])
                )
                for i in range(len(timestamps))
                if all(quote_data[field][i] is not None for field in
                       ['open', 'low', 'high', 'close'])
                and adj_close_data[i] is not None
            ]

            if output == OutputFormat.DICT:
                return processed_data
            raise TransformerException("Output format invalid")

        except (KeyError, ValueError) as e:
            raise TransformerException(
                "Transformation failed due to missing keys or value errors."
            ) from e
        except Exception as e:
            raise TransformerException("Transformation failed due to an unexpected error.") from e

    @staticmethod
    def transform_single_data(timestamp: int, price_values: tuple) -> Dict[str, Any]:
        """
        Transforms a single dataset from transform_results.

        Args:
            timestamp (int): Unix timestamp.
            price_values (tuple): Tuple containing open, low, high, close, and adjclose prices.

        Returns:
            Dict[str, Any]: A dictionary containing the transformed data.
        """
        return {
            "timestamp": timestamp,
            "open": price_values[0],
            "low": price_values[1],
            "high": price_values[2],
            "close": price_values[3],
            "adjclose": price_values[4],
        }

    @classmethod
    def output(cls, data: str, output: str) -> Union[str, List[Dict[Any, Any]]]:
        """
        Takes raw JSON from API response and converts/formats it.

        Args:
            data (str): Raw JSON as input.
            output (str): Desired output format (OutputFormat).

        Returns:
            Union[str, List[Dict[Any, Any]]]: Converted and formatted data.

        Raises:
            TransformerException: If output format is invalid.
        """
        if output == OutputFormat.DICT.value:
            return cls.transform_results(data, OutputFormat.DICT)
        if output == OutputFormat.RAW.value:
            return data
        raise TransformerException("Output format invalid")
