"""
Module: Transformer

Copyright 2023 Dominic Kneup.
Licensed under the MIT License; you can find the LICENSE file in the project's root folder.
"""
import json
from typing import List, Dict, Any


class Transformer:
    """
    Class for transforming JSON data.
    """
    @staticmethod
    def json_to_list(response: str) -> List[Any]:
        """
        Converts a JSON string into a list.

        Args:
            response (str): The JSON string to convert.

        Returns:
            List[Any]: The converted list.

        Raises:
            ValueError: If the input is not a valid JSON string.
        """
        try:
            return json.loads(response)
        except json.JSONDecodeError as e:
            raise ValueError(f"Invalid JSON: {e}") from e

    @staticmethod
    def flatten_dict(data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Flattens a multi-dimensional dictionary into a 1-dimensional one.

        Args:
            data (Dict[str, Any]): The dictionary to flatten.

        Returns:
            Dict[str, Any]: The flattened dictionary.
        """
        converted = {}
        for key, value in data.items():
            if isinstance(value, dict) and 'raw' in value:
                converted[key] = value['raw']
            elif isinstance(value, (str, int, float)):
                converted[key] = value
            elif isinstance(value, list):
                # Convert list to a string representation
                converted[key] = ','.join(map(str, value))
            else:
                raise ValueError(f"Unsupported value type: {type(value)}")
        return converted
