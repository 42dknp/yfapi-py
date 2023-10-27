"""
Module: Quote

Copyright 2023 Dominic Kneup.
Licensed under the MIT License; you can find the LICENSE file in the project's root folder.
"""
from typing import Union
from client.api.crumb import Crumb
from client.api.validators.validator import Validator
from client.api.transformers.quote_transformer import QuoteTransformer


class Quote(Crumb):
    """
    Class Quote
    Attributes:
        endpoint (str): api Endpoint URL (optional)
        allowedFields (list): Allowed fields for api Call (optional)
        corsDomain (str): Setup CorsDomain (Optional)
        region (str): Setup Region (optional)
        language (str): Setup Language (optional)
        formatted (str): Setup api Output Format (should only used with "raw" json output, Optional)
        output (str): Setup Default client Output Format (optional)
        crumb (str): Setup existing Crumb (optional)
    """
    # api Endpoint URL
    endpoint: str = "https://query2.finance.yahoo.com/v7/finance/quote"

    # Allowed fields for api Call
    allowedFields: list = [
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

    # Setup CorsDomain
    corsDomain: str = "finance.yahoo.com"

    # Setup Region
    region: str = "US"

    # Setup Language
    language: str = "en-US"

    # Setup Output Format
    formatted: str = "true"

    # Setup Default Output Format
    output: str = "dict"

    # Setup Crumb (optional)
    crumb: str = ""

    def get_quote(self, symbol: str) \
            -> Union[str, dict, list]:
        """
        Get Quote by Symbol (Security)
        @param symbol: The Security / Stock symbol
        @return: Returns raw json output / formatted List or Dict
        """
        # If crumb is emtpy
        if self.crumb == "":
            # Get a new Crumb
            self.crumb = self.get_crumb()

        params = {
            'formatted': self.formatted,
            'crumb': self.crumb,
            'lang': self.language,
            'region': self.region,
            'symbols': symbol,
            'fields': QuoteTransformer.transform_fields(self.allowedFields, self.allowedFields),
            'corsDomain': self.corsDomain
        }

        response = self.request_api(self.endpoint, params)

        # Check response for errors
        Validator.check_response_error(response)

        quote = QuoteTransformer.output(response, self.output)

        return quote
