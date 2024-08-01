"""
Module: Quote

Copyright 2023 Dominic Kneup.
Licensed under the MIT License; you can find the LICENSE file in the project's root folder.
"""
import logging
from typing import Union, List, Dict
from client.api.crumb import Crumb
from client.api.transformers.quote_transformer import QuoteTransformer
from client.api.config import settings
from client.exceptions.APIClientExceptions import ApiException

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class Quote(Crumb):
    """
    Class Quote
    Attributes:
        endpoint (str): API Endpoint URL
        allowedFields (list): Allowed fields for API Call
        cors_domain (str): CORS Domain
        region (str): Region
        language (str): Language
        formatted (str): API Output Format
        output (str): Default client Output Format
        crumb (str): Existing Crumb
    """
    allowedFields: List[str] = [
        "longName",
        "shortName",
        "regularMarketPrice",
        "regularMarketChange",
        "regularMarketChangePercent",
        "messageBoardId",
        "marketCap",
        "underlyingSymbol",
        "underlyingExchangeSymbol",
        "headSymbolAsString",
        "regularMarketVolume",
        "uuid",
        "regularMarketOpen",
        "fiftyTwoWeekLow",
        "fiftyTwoWeekHigh",
        "toCurrency",
        "fromCurrency",
        "toExchange",
        "fromExchange",
        "corporateActions"
    ]

    def __init__(self,
                 endpoint: str = settings.quote_api_endpoint,
                 cors_domain: str = settings.quote_cors_domain,
                 region: str = settings.quote_region,
                 language: str = settings.quote_language,
                 formatted: str = settings.quote_formatted,
                 output: str = settings.quote_output,):
        super().__init__()
        self.endpoint = endpoint
        self.cors_domain = cors_domain
        self.region = region
        self.language = language
        self.formatted = formatted
        self.output = output
        self.crumb = self.get_crumb()

    def get_quote(self, symbol: str) -> Union[str, Dict, List]:
        """
        Get Quote by Symbol (Security)
        @param symbol: The Security / Stock symbol
        @return: Returns raw JSON output / formatted List or Dict
        """
        logger.info("Fetching quote for symbol: %s", symbol)

        if not self.crumb:
            logger.info("Crumb is empty, fetching new crumb")
            self.crumb = self.get_crumb()

        params = {
            'formatted': self.formatted,
            'crumb': self.crumb,
            'lang': self.language,
            'region': self.region,
            'symbols': symbol,
            'fields': QuoteTransformer.transform_fields(
                fields=self.allowedFields,
                allowed_fields=self.allowedFields
            ),
            'cors_domain': self.cors_domain
        }
        print(self.crumb)
        try:
            response_data = self.request_api(self.endpoint, params=params)

            quote = QuoteTransformer.output(data=response_data, output=self.output)
            logger.info("Successfully fetched quote for symbol: %s", symbol)
            return quote

        except ApiException as e:
            logger.error("API error fetching quote for symbol %s: %s", symbol, e)
            raise
        except Exception as e:
            logger.error("Unexpected error fetching quote for symbol %s: %s", symbol, e)
            raise
