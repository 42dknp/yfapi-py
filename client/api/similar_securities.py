"""
Module: SimilarSecurities

Copyright 2023 Dominic Kneup.
Licensed under the MIT License; you can find the LICENSE file in the project's root folder.
"""
from typing import Union
from client.api_client import ApiClient
from client.api.validators.validator import Validator
from client.api.transformers.similar_securities_transformer import SimilarSecuritiesTransformer


class SimilarSecurities(ApiClient):
    """
    Class SimilarSecurities
    Attributes:
        apiEndpoint (str): api Endpoint URL (optional)
        output (str): Setup Default Output Format (optional)
    """

    # Yahoo Finance api Endpoint to request similar Securities
    apiEndpoint: str = "https://query2.finance.yahoo.com/v6/finance/recommendationsbysymbol/"

    # Setup Default Output Format
    output: str = "list"

    def get_similar_securities(self, security) -> Union[str, list]:
        """
        Get similar Securities api Call
        @param security: The Security Symbol to get information for (e.g. AMD)
        @return: A list of similar securities or raw json api response
        """
        url: str = self.apiEndpoint + security

        # Get Similar Securities
        response: str = self.request_api(url)

        # Check response for errors
        Validator.check_response_error(response)

        return SimilarSecuritiesTransformer.output(response, self.output)
