"""
Module: CrumbValidator

Copyright 2023 Dominic Kneup.
Licensed under the MIT License; you can find the LICENSE file in the project's root folder.
"""
from client.exceptions.APIClientExceptions import ValidatorException


class CrumbValidator:
    """
    Provides validation for crumb strings.
    """
    @staticmethod
    def validate_crumb(crumb: str) -> str:
        """
        Validates that the crumb is not empty.

        Args:
            crumb (str): The crumb string to validate.

        Returns:
            str: The valid crumb string.

        Raises:
            ValidatorException: If the crumb is empty.
        """
        if crumb != '':
            return crumb
        raise ValidatorException("Crumb generation failed.")
