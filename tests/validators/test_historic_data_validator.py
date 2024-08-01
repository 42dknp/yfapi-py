# Copyright 2023 Dominic Kneup.
# Licensed under the MIT License; you can find the LICENSE file in the project's root folder.

import unittest, json
from client.api.validators.historic_data_validator import HistoricDataValidator
from parameterized import parameterized

class HistoricDataValidatorTest(unittest.TestCase):
    def setUp(self):
        self.data_object = self._load_test_data()

    @parameterized.expand([
        ('currency', 'Missing currency property'),
        ('symbol', 'Missing symbol property'),
        ('exchangeName', 'Missing exchangeName property'),
        ('regularMarketPrice', 'Missing regularMarketPrice property'),
    ])
    def test_validate_meta_properties_with_missing_property(self, property_name, error_message):
        data_missing = self.data_object
        del data_missing['chart']['result'][0]['meta'][property_name]
        with self.assertRaises(Exception) as context:
            HistoricDataValidator.validate_results(data_missing)
        self.assertEqual(str(context.exception), error_message)

    @parameterized.expand([
        ('volume', 'Invalid sub-properties for volume'),
        ('open', 'Invalid sub-properties for open'),
        ('close', 'Invalid sub-properties for close'),
        ('high', 'Invalid sub-properties for high'),
        ('low', 'Invalid sub-properties for low'),
    ])
    def test_validate_quote_properties_with_missing_subproperty(self, property_name, error_message):
        data_missing = self.data_object
        del data_missing['chart']['result'][0]['indicators']['quote'][0][property_name]
        with self.assertRaises(Exception) as context:
            HistoricDataValidator.validate_results(data_missing)
        self.assertEqual(str(context.exception), error_message)

    def test_map_data_to_object_with_valid_data(self):
        self.assertNotEqual(HistoricDataValidator.validate_results(self.data_object), False)

    def test_validate_results_with_missing_meta_property(self):
        data_missing = self.data_object
        del data_missing['chart']['result'][0]['meta']
        with self.assertRaises(Exception):
            HistoricDataValidator.validate_results(data_missing)

    def test_validate_results_with_missing_quote_properties(self):
        data_missing = self.data_object
        del data_missing['chart']['result'][0]['indicators']['quote']
        with self.assertRaises(Exception):
            HistoricDataValidator.validate_results(data_missing)

    def test_validate_adjclose_properties_with_missing_adjclose(self):
        data_missing = self.data_object
        del data_missing['chart']['result'][0]['indicators']['adjclose'][0]
        with self.assertRaises(Exception) as context:
            HistoricDataValidator.validate_results(data_missing)
        self.assertEqual(str(context.exception), 'Missing adjclose property')

    @staticmethod
    def _load_test_data():
        data = ('{"chart":{"result":[{"meta":{"currency":"USD","symbol":"GS","exchangeName":"NYQ",'
                '"instrumentType":"EQUITY","firstTradeDate":925824600,"regularMarketTime":1696881602,'
                '"gmtoffset":-14400,"timezone":"EDT","exchangeTimezoneName":"America/New_York",'
                '"regularMarketPrice":312.61,"chartPreviousClose":323.57,"priceHint":2,"currentTradingPeriod":{'
                '"pre":{"timezone":"EDT","start":1696924800,"end":1696944600,"gmtoffset":-14400},"regular":{'
                '"timezone":"EDT","start":1696944600,"end":1696968000,"gmtoffset":-14400},"post":{"timezone":"EDT",'
                '"start":1696968000,"end":1696982400,"gmtoffset":-14400}},"dataGranularity":"1d","range":"",'
                '"validRanges":["1d","5d","1mo","3mo","6mo","1y","2y","5y","10y","ytd","max"]},"timestamp":['
                '1696253400,1696339800,1696426200,1696512600,1696599000,1696858200],"indicators":{"quote":[{"low":['
                '317.1000061035156,304.3900146484375,303.4800109863281,304.2099914550781,307.1700134277344,'
                '308.3699951171875],"volume":[1303800,3118600,1872000,1584600,1595100,1094400],'
                '"open":[322.0299987792969,315.2699890136719,304.8500061035156,307.3599853515625,308.1099853515625,'
                '308.8999938964844],"close":[318.5,306.1199951171875,308.6000061035156,310.5,312.4800109863281,'
                '312.6099853515625],"high":[323.5799865722656,315.67999267578125,309.05999755859375,'
                '310.54998779296875,315.32000732421875,313.4800109863281]}],"adjclose":[{"adjclose":[318.5,'
                '306.1199951171875,308.6000061035156,310.5,312.4800109863281,312.6099853515625]}]}}],"error":null}}')
        return json.loads(data)
