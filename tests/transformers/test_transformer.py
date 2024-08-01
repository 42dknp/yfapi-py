# Copyright 2023 Dominic Kneup.
# Licensed under the MIT License; you can find the LICENSE file in the project's root folder.
import json
import unittest
from parameterized import parameterized
from client.api.transformers.transformer import Transformer


class TestTransformer(unittest.TestCase):

    def setUp(self):
        """
        Setup Demo data (actual api response) for testing
        """
        data = ('{"quoteResponse":{"result":[{"fullExchangeName":"NasdaqGS","symbol":"AMD",'
                '"fiftyTwoWeekLowChangePercent":{"raw":0.9931281,"fmt":"99.31%"},"gmtOffSetMilliseconds":-14400000,'
                '"regularMarketOpen":{"raw":109.14,"fmt":"109.14"},"language":"en-US","regularMarketTime":{'
                '"raw":1697035260,"fmt":"10:41AM EDT"},"regularMarketChangePercent":{"raw":-0.22475255,'
                '"fmt":"-0.22%"},"uuid":"48af4341-f745-363f-945f-a838eeabb062","quoteType":"EQUITY",'
                '"regularMarketDayRange":{"raw":"107.89 - 110.1","fmt":"107.89 - 110.10"},"fiftyTwoWeekLowChange":{'
                '"raw":54.195,"fmt":"54.19"},"fiftyTwoWeekHighChangePercent":{"raw":-0.18117143,"fmt":"-18.12%"},'
                '"regularMarketDayHigh":{"raw":110.1,"fmt":"110.10"},"typeDisp":"Equity","tradeable":false,'
                '"currency":"USD","sharesOutstanding":{"raw":1615670016,"fmt":"1.616B","longFmt":"1,615,670,016"},'
                '"fiftyTwoWeekHigh":{"raw":132.83,"fmt":"132.83"},"regularMarketPreviousClose":{"raw":109.01,'
                '"fmt":"109.01"},"exchangeTimezoneName":"America/New_York","fiftyTwoWeekHighChange":{'
                '"raw":-24.065002,"fmt":"-24.07"},"marketCap":{"raw":175728345088,"fmt":"175.728B","longFmt":"175,'
                '728,345,088"},"regularMarketChange":{"raw":-0.24500275,"fmt":"-0.25"},"fiftyTwoWeekRange":{'
                '"raw":"54.57 - 132.83","fmt":"54.57 - 132.83"},"cryptoTradeable":false,"exchangeDataDelayedBy":0,'
                '"firstTradeDateMilliseconds":322151400000,"exchangeTimezoneShortName":"EDT","regularMarketPrice":{'
                '"raw":108.765,"fmt":"108.76"},"fiftyTwoWeekLow":{"raw":54.57,"fmt":"54.57"},"marketState":"REGULAR",'
                '"customPriceAlertConfidence":"HIGH","market":"us_market","regularMarketVolume":{"raw":14020928,'
                '"fmt":"14.021M","longFmt":"14,020,928"},"quoteSourceName":"Nasdaq Real Time Price",'
                '"messageBoardId":"finmb_168864","priceHint":2,"regularMarketDayLow":{"raw":107.89,"fmt":"107.89"},'
                '"exchange":"NMS","sourceInterval":15,"region":"US","shortName":"Advanced Micro Devices, Inc.",'
                '"triggerable":true,"corporateActions":[],"longName":"Advanced Micro Devices, Inc."}],"error":null}}')

        # Convert json string to object for further use
        self.data_object = json.loads(data)

    @parameterized.expand([
        ('{"fullExchangeName": "NasdaqGS"}', {'fullExchangeName': 'NasdaqGS'}),
    ])
    def test_json_to_list_valid_json(self, valid_json, expected_data):
        """
        Test converting valid JSON string to list
        """
        decoded_data = Transformer.json_to_list(valid_json)
        self.assertEqual(expected_data, decoded_data)

    @parameterized.expand([
        ('{"key": "value",}', ValueError),
        ('', ValueError),
    ])
    def test_json_to_list_invalid_json(self, invalid_json, expected_exception):
        """
        Test converting invalid JSON string to list
        """
        with self.assertRaises(expected_exception):
            Transformer.json_to_list(invalid_json)

    @parameterized.expand([
        ({
            'fullExchangeName': 'NasdaqGS',
            'exchangeTimezoneShortName': "EDT",
        }, {
            'fullExchangeName': 'NasdaqGS',
            'exchangeTimezoneShortName': "EDT",
        }),
        ({
            'fullExchangeName': 'NasdaqGS',
            'fiftyTwoWeekLowChangePercent': {'raw': 0.9931281},
        }, {
            'fullExchangeName': 'NasdaqGS',
            'fiftyTwoWeekLowChangePercent': 0.9931281,
        }),
        ({
            'symbol': 'AMD',
            'language': 'en-US',
            'fiftyTwoWeekLowChangePercent': {'raw': 0.9931281},
            'regularMarketDayLow': {'raw': 107.89},
        }, {
            'symbol': 'AMD',
            'language': 'en-US',
            'fiftyTwoWeekLowChangePercent': 0.9931281,
            'regularMarketDayLow': 107.89,
        }),
        ({}, {}),
    ])
    def test_flatten_dict(self, data, expected_data):
        """
        Test flattening of data with various input scenarios
        """
        flattened_data = Transformer.flatten_dict(data)
        self.assertEqual(expected_data, flattened_data)
