"""
Module: HistoricDataTransformer

Copyright 2023 Dominic Kneup.
Licensed under the MIT License; you can find the LICENSE file in the project's root folder.
"""
from typing import Union, List, Dict, Any
from client.api.transformers.transformer import Transformer
from client.api.validators.historic_data_validator import HistoricDataValidator
from client.exceptions.APIClientExceptions import TransformerException


class HistoricDataTransformer:
    """
    Class HistoricDataTransformer
    """
    OUTPUT_DICT = "dict"
    OUTPUT_RAW = "raw"

    @staticmethod
    def transform_results(result: str, output: str) -> List[Any]:
        """
        Validates and Transforms  Historic data
        @param result: string, The raw json from api as input
        @param output: list, Defines the output format
        @return: A list with Historic data
        """
        try:
            data = dict(Transformer.decode_json_response(result))

            HistoricDataValidator.validate_results(data)

            timestamps = data['chart']['result'][0]['timestamp']
            quote_data = data['chart']['result'][0]['indicators']['quote'][0]
            adj_close_data = data['chart']['result'][0]['indicators']['adjclose'][0]['adjclose']

            processed_data: List[Union[dict, object]] = []

            for i, _ in enumerate(timestamps):
                if (
                        quote_data['open'][i] is None
                        or quote_data['low'][i] is None
                        or quote_data['high'][i] is None
                        or quote_data['close'][i] is None
                        or adj_close_data[i] is None
                ):
                    continue

                processed_data.append(
                    dict(HistoricDataTransformer.transform_single_data(
                        timestamps[i],
                        (quote_data['open'][i],
                         quote_data['low'][i],
                         quote_data['high'][i],
                         quote_data['close'][i],
                         adj_close_data[i])
                    ))
                )

            if output == HistoricDataTransformer.OUTPUT_DICT:
                return processed_data
            raise TransformerException("Output format invalid")

        except Exception as e:
            raise TransformerException("Transformation failed.") from e

    @staticmethod
    def transform_single_data(
            timestamp: int, price_values: tuple
    ) -> Union[dict, List[Any]]:
        """
        Transforms single datasets from transform_results
        @param timestamp: integer, date and time in the Unix format
        @param price_values: tuple with floats, contains open, low, high, close and adjclose prices
        dividends and stock splits for accurate historical analysis.
        @return: List or Dict
        """
        dataset = {
            "timestamp": timestamp,
            "open": price_values[0],
            "low": price_values[1],
            "high": price_values[2],
            "close": price_values[3],
            "adjclose": price_values[4],
        }
        # Return a dictionary or list based on the output
        return dataset

    @classmethod
    def output(cls, data: str, output: str) -> Union[str, List[Dict[Any, Any]]]:
        """
        Takes raw json from api response and converts / formats it
        @param data: string, raw json as input
        @param output: string, either raw, list or dict
        @return: [string, dict or list] Returns converted and formatted data
        """
        if output == cls.OUTPUT_DICT:
            return cls.transform_results(data, output)
        if output == cls.OUTPUT_RAW:
            return data
        raise TransformerException("Output format invalid")
