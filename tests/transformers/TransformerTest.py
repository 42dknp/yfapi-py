# Copyright 2023 Dominic Kneup.
# Licensed under the MIT License; you can find the LICENSE file in the project's root folder.
import json
import unittest
from client.api.transformers.transformer import Transformer


class TransformerTest(unittest.TestCase):
    data_object = None

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

    def test_decodeJsonResponse_valid_json(self):
        valid_json = '{"fullExchangeName": "NasdaqGS"}'

        decoded_data = Transformer.decode_json_response(valid_json)

        # Expected value should be a dictionary
        expected_data = {'fullExchangeName': 'NasdaqGS'}

        self.assertEqual(expected_data, decoded_data)

    def test_decodeJsonResponse_invalid_json(self):
        invalid_json = '{"key": "value",}'  # Invalid JSON due to trailing comma

        with self.assertRaises(Exception):
            Transformer.decode_json_response(invalid_json)

    def test_decode_json_response_empty_json(self):
        empty_json = ''

        with self.assertRaises(Exception) as context:
            Transformer.decode_json_response(empty_json)

        self.assertEqual('Expecting value: line 1 column 1 (char 0)', str(context.exception))

    def test_flattenData_with_string_value(self):
        data = {
            'fullExchangeName': self.data_object['quoteResponse']['result'][0]['fullExchangeName'],
            'exchangeTimezoneShortName': self.data_object['quoteResponse']['result'][0]['exchangeTimezoneShortName'],
        }

        flattened_data = Transformer.flatten_data(data)

        expected_data = {
            'fullExchangeName': 'NasdaqGS',
            'exchangeTimezoneShortName': "EDT",
        }

        self.assertEqual(expected_data, flattened_data)

    def test_flattenData_with_raw_value(self):
        data = {
            'fullExchangeName': self.data_object['quoteResponse']['result'][0]['fullExchangeName'],
            'fiftyTwoWeekLowChangePercent': {
                'raw': self.data_object['quoteResponse']['result'][0]['fiftyTwoWeekLowChangePercent']['raw']},
        }

        flattened_data = Transformer.flatten_data(data)

        expected_data = {
            'fullExchangeName': self.data_object['quoteResponse']['result'][0]['fullExchangeName'],
            'fiftyTwoWeekLowChangePercent':
                self.data_object['quoteResponse']['result'][0]['fiftyTwoWeekLowChangePercent']['raw'],
        }

        self.assertEqual(expected_data, flattened_data)

    def test_flattenData_with_mixed_values(self):
        data = {
            'symbol': self.data_object['quoteResponse']['result'][0]['symbol'],
            'language': self.data_object['quoteResponse']['result'][0]['language'],
            'fiftyTwoWeekLowChangePercent': {
                'raw': self.data_object['quoteResponse']['result'][0]['fiftyTwoWeekLowChangePercent']['raw']},
            'regularMarketDayLow': {
                'raw': self.data_object['quoteResponse']['result'][0]['regularMarketDayLow']['raw']},
        }

        flattened_data = Transformer.flatten_data(data)

        expected_data = {
            'symbol': self.data_object['quoteResponse']['result'][0]['symbol'],
            'language': self.data_object['quoteResponse']['result'][0]['language'],
            'fiftyTwoWeekLowChangePercent':
                self.data_object['quoteResponse']['result'][0]['fiftyTwoWeekLowChangePercent']['raw'],
            'regularMarketDayLow': self.data_object['quoteResponse']['result'][0]['regularMarketDayLow']['raw'],
        }

        self.assertEqual(expected_data, flattened_data)

    def test_flattenData_with_empty_array(self):
        data = {}

        flattened_data = Transformer.flatten_data(data)

        self.assertIsInstance(flattened_data, dict)
        self.assertDictEqual({}, flattened_data)
