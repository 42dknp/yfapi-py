"""
Module: SimilarSecurities

Copyright 2023 Dominic Kneup.
Licensed under the MIT License; you can find the LICENSE file in the project's root folder.
"""
import logging
from typing import Union
from client.api_client import ApiClient
from client.api.validators.validator import Validator
from client.exceptions.APIClientExceptions import ApiException
from client.api.transformers.similar_securities_transformer import SimilarSecuritiesTransformer
from client.api.config import settings

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class SimilarSecurities(ApiClient):
    """
    Class SimilarSecurities
    Attributes:
        apiEndpoint (str): api Endpoint URL (optional)
        output (str): Setup Default Output Format (optional)
    """
    def __init__(
            self,
            api_endpoint: str = settings.similar_securities_api_endpoint,
            output_format: str = settings.similar_securities_output):
        super().__init__()
        self.api_endpoint = api_endpoint
        self.output_format = output_format

    def get_similar_securities(self, security_symbol: str) -> Union[str, list]:
        """
        Get similar Securities api Call
        @param security: The Security Symbol to get information for (e.g. AMD)
        @return: A list of similar securities or raw json api response
        """
        logger.info("Fetching similar securities for: %s", security_symbol)

        try:
            url = f"{self.api_endpoint}{security_symbol}"
            response_data = self.request_api(url)

            Validator.check_response_error(response_data)
            similar_securities = SimilarSecuritiesTransformer.output(
                response_data,
                self.output_format
            )
            logger.info("Successfully fetched similar securities for: %s", security_symbol)

            return similar_securities

        except ApiException as e:
            logger.error("API error fetching similar securities for %s: %s", security_symbol, e)
            raise
        except Exception as e:
            logger.error(
                "Unexpected error fetching similar securities for %s: %s", security_symbol, e
            )
            raise
