# Copyright 2023 Dominic Kneup.
# Licensed under the MIT License; you can find the LICENSE file in the project's root folder.

import unittest, json
from client.api.validators.quote_validator import QuoteValidator


class QuoteValidatorTest(unittest.TestCase):
    def setUp(self):
        """
        Setup Demo data (actual api response) for testing
        """
        data = ('{"quoteResponse":{"result":[{"fullExchangeName":"NasdaqGS","symbol":"AAPL",'
                '"fiftyTwoWeekLowChangePercent":{"raw":0.42941135,"fmt":"42.94%"},"gmtOffSetMilliseconds":-14400000,'
                '"regularMarketOpen":{"raw":173.8,"fmt":"173.80"},"language":"en-US","regularMarketTime":{'
                '"raw":1696622402,"fmt":"4:00PM EDT"},"regularMarketChangePercent":{"raw":1.4750453,"fmt":"1.48%"},'
                '"uuid":"8b10e4ae-9eeb-3684-921a-9ab27e4d87aa","quoteType":"EQUITY","regularMarketDayRange":{'
                '"raw":"173.18 - 177.99","fmt":"173.18 - 177.99"},"fiftyTwoWeekLowChange":{"raw":53.320007,'
                '"fmt":"53.32"},"fiftyTwoWeekHighChangePercent":{"raw":-0.104625896,"fmt":"-10.46%"},'
                '"regularMarketDayHigh":{"raw":177.99,"fmt":"177.99"},"typeDisp":"Equity","tradeable":false,'
                '"currency":"USD","sharesOutstanding":{"raw":15634199552,"fmt":"15.634B","longFmt":"15,634,199,552"},'
                '"fiftyTwoWeekHigh":{"raw":198.23,"fmt":"198.23"},"regularMarketPreviousClose":{"raw":174.91,'
                '"fmt":"174.91"},"exchangeTimezoneName":"America/New_York","fiftyTwoWeekHighChange":{"raw":-20.73999,'
                '"fmt":"-20.74"},"marketCap":{"raw":2774914039808,"fmt":"2.775T","longFmt":"2,774,914,039,808"},'
                '"regularMarketChange":{"raw":2.5800018,"fmt":"2.58"},"fiftyTwoWeekRange":{"raw":"124.17 - 198.23",'
                '"fmt":"124.17 - 198.23"},"cryptoTradeable":false,"exchangeDataDelayedBy":0,'
                '"firstTradeDateMilliseconds":345479400000,"exchangeTimezoneShortName":"EDT","fiftyTwoWeekLow":{'
                '"raw":124.17,"fmt":"124.17"},"customPriceAlertConfidence":"HIGH","regularMarketPrice":{"raw":177.49,'
                '"fmt":"177.49"},"marketState":"PRE","regularMarketVolume":{"raw":57266675,"fmt":"57.267M",'
                '"longFmt":"57,266,675"},"market":"us_market","quoteSourceName":"Delayed Quote",'
                '"messageBoardId":"finmb_24937","priceHint":2,"regularMarketDayLow":{"raw":173.18,"fmt":"173.18"},'
                '"exchange":"NMS","sourceInterval":15,"shortName":"Apple Inc.","region":"US","triggerable":true,'
                '"corporateActions":[],"longName":"Apple Inc."}],"error":null}}')
        self.data_object = json.loads(data)

    def test_map_data_to_object(self):
        self.assertIsNone(QuoteValidator.validate_results(self.data_object))

    def test_valid_data(self):
        self.assertIsNone(QuoteValidator.validate_results(self.data_object))

    def test_additional_sub_properties(self):
        if 'fiftyTwoWeekLowChange' not in self.data_object['quoteResponse']['result'][0]:
            self.data_object['quoteResponse']['result'][0]['fiftyTwoWeekLowChange'] = {}
        self.assertIsNone(QuoteValidator.validate_results(self.data_object))

    def test_missing_required_property(self):
        data_object = self.data_object
        del data_object['quoteResponse']['result'][0]['symbol']

        with self.assertRaises(Exception) as cm:
            QuoteValidator.validate_results(data_object)

        self.assertEqual(str(cm.exception), "Missing symbol property")

    def test_missing_sub_properties(self):
        data_object = self.data_object
        data_object['quoteResponse']['result'][0]['fiftyTwoWeekLowChange'] = {}

        with self.assertRaises(Exception) as cm:
            QuoteValidator.validate_results(data_object)

        self.assertEqual(str(cm.exception), "Invalid sub-properties for fiftyTwoWeekLowChange")

    def test_invalid_sub_property(self):
        data_object = self.data_object
        data_object['quoteResponse']['result'][0]['regularMarketDayLow'] = {"invalidProperty": 'invalid'}

        with self.assertRaises(Exception) as cm:
            QuoteValidator.validate_results(data_object)

        self.assertEqual(str(cm.exception), "Invalid sub-properties for regularMarketDayLow")


if __name__ == '__main__':
    unittest.main()
