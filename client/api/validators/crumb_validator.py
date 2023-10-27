"""
Module: CrumbValidator

Copyright 2023 Dominic Kneup.
Licensed under the MIT License; you can find the LICENSE file in the project's root folder.
"""
from client.exceptions.APIClientExceptions import ValidatorException


class CrumbValidator:
    """
    Class: CrumbValidator
    """

    @staticmethod
    def validate_crumb(crumb: str) -> str:
        """
        Validate that the crumb is not empty.
        @param crumb: Crumb as string
        @return: string, returns the crumb if valid
        """
        if crumb != '':
            return crumb
        raise ValidatorException("Crumb generation failed.")
