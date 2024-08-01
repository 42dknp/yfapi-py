"""
Module: HistoricDataTransformer_Test

Copyright 2023 Dominic Kneup.
Licensed under the MIT License; you can find the LICENSE file in the project's root folder.
"""
import unittest
from client.api.transformers.historic_data_transformer import HistoricDataTransformer, OutputFormat
from client.exceptions.APIClientExceptions import TransformerException
from parameterized import parameterized


class TestHistoricDataTransformer(unittest.TestCase):
    def setUp(self):
        """
        Setup Demo data (actual api response) for testing
        """
        self.json = ('{"chart":{"result":[{"meta":{"currency":"USD","symbol":"GS","exchangeName":"NYQ",'
                     '"instrumentType":"EQUITY","firstTradeDate":925824600,"regularMarketTime":1696881602,'
                     '"gmtoffset":-14400,"timezone":"EDT","exchangeTimezoneName":"America/New_York",'
                     '"regularMarketPrice":312.61,"chartPreviousClose":323.57,"priceHint":2,"currentTradingPeriod":{'
                     '"pre":{"timezone":"EDT","start":1696924800,"end":1696944600,"gmtoffset":-14400},"regular":{'
                     '"timezone":"EDT","start":1696944600,"end":1696968000,"gmtoffset":-14400},'
                     '"post":{"timezone":"EDT","start":1696968000,"end":1696982400,"gmtoffset":-14400}},'
                     '"dataGranularity":"1d","range":"","validRanges":["1d","5d","1mo","3mo","6mo","1y","2y","5y",'
                     '"10y","ytd","max"]},"timestamp":[1696253400,1696339800,1696426200,1696512600,1696599000,'
                     '1696858200],"indicators":{"quote":[{"low":[317.1000061035156,304.3900146484375,'
                     '303.4800109863281,304.2099914550781,307.1700134277344,308.3699951171875],"volume":[1303800,'
                     '3118600,1872000,1584600,1595100,1094400],"open":[322.0299987792969,315.2699890136719,'
                     '304.8500061035156,307.3599853515625,308.1099853515625,308.8999938964844],"close":[318.5,'
                     '306.1199951171875,308.6000061035156,310.5,312.4800109863281,312.6099853515625],'
                     '"high":[323.5799865722656,315.67999267578125,309.05999755859375,310.54998779296875,'
                     '315.32000732421875,313.4800109863281]}],"adjclose":[{"adjclose":[318.5,306.1199951171875,'
                     '308.6000061035156,310.5,312.4800109863281,312.6099853515625]}]}}],"error":null}}')

    @parameterized.expand([
        (OutputFormat.DICT, 6)
    ])
    def test_transform_results(self, output_format, expected_count):
        actual = HistoricDataTransformer.transform_results(self.json, output_format)
        self.assertEqual(len(actual), expected_count)

        # Ensure the transformed data contains expected keys
        self.assertIn('timestamp', actual[0])
        self.assertIn('open', actual[0])
        self.assertIn('low', actual[0])
        self.assertIn('high', actual[0])
        self.assertIn('close', actual[0])
        self.assertIn('adjclose', actual[0])

    @parameterized.expand([
        (1696253400, 322.0299987792969, 317.1000061035156, 323.5799865722656, 318.5, 318.5)
    ])
    def test_transform_single_data(self, timestamp, open_val, low, high, close, adj_close):
        expected_array = {
            'timestamp': timestamp,
            'open': open_val,
            'low': low,
            'high': high,
            'close': close,
            'adjclose': adj_close
        }

        actual_array = HistoricDataTransformer.transform_single_data(timestamp, (open_val, low, high, close, adj_close))
        self.assertEqual(expected_array, actual_array)

    def test_output(self):
        expected_array_output = [
            {
                'timestamp': 1696253400,
                'open': 322.0299987792969,
                'low': 317.1000061035156,
                'high': 323.5799865722656,
                'close': 318.5,
                'adjclose': 318.5,
            },
            {
                'timestamp': 1696339800,
                'open': 315.2699890136719,
                'low': 304.3900146484375,
                'high': 315.67999267578125,
                'close': 306.1199951171875,
                'adjclose': 306.1199951171875,
            },
            {
                'timestamp': 1696426200,
                'open': 304.8500061035156,
                'low': 303.4800109863281,
                'high': 309.05999755859375,
                'close': 308.6000061035156,
                'adjclose': 308.6000061035156,
            },
            {
                'timestamp': 1696512600,
                'open': 307.3599853515625,
                'low': 304.2099914550781,
                'high': 310.54998779296875,
                'close': 310.5,
                'adjclose': 310.5,
            },
            {
                'timestamp': 1696599000,
                'open': 308.1099853515625,
                'low': 307.1700134277344,
                'high': 315.32000732421875,
                'close': 312.4800109863281,
                'adjclose': 312.4800109863281,
            },
            {
                'timestamp': 1696858200,
                'open': 308.8999938964844,
                'low': 308.3699951171875,
                'high': 313.4800109863281,
                'close': 312.6099853515625,
                'adjclose': 312.6099853515625,
            },
        ]

        actual_list_output = HistoricDataTransformer.output(self.json, 'dict')
        self.assertEqual(1696253400, actual_list_output[0]["timestamp"])
        self.assertEqual(303.4800109863281, actual_list_output[2]["low"])
        self.assertEqual(312.4800109863281, actual_list_output[4]["adjclose"])
        self.assertEqual(308.8999938964844, actual_list_output[5]["open"])

        actual_object_output = HistoricDataTransformer.output(self.json, 'dict')
        self.assertEqual(expected_array_output, actual_object_output)

    def test_invalid_json(self):
        invalid_json = '{"chart": {"result": [}}'
        with self.assertRaises(TransformerException):
            HistoricDataTransformer.transform_results(invalid_json, OutputFormat.DICT)

    def test_missing_keys(self):
        missing_keys_json = '{"chart": {"result": [{}]}}'
        with self.assertRaises(TransformerException):
            HistoricDataTransformer.transform_results(missing_keys_json, OutputFormat.DICT)

    def test_empty_data(self):
        empty_data_json = '{"chart": {"result": [{"timestamp": [], "indicators": {"quote": [{}], "adjclose": [{}]}}]}}'
        with self.assertRaises(TransformerException):
            HistoricDataTransformer.transform_results(empty_data_json, OutputFormat.DICT)

    def test_invalid_output_format(self):
        with self.assertRaises(TransformerException):
            HistoricDataTransformer.transform_results(self.json, "invalid_format")

    def test_none_values(self):
        none_values_json = ('{"chart":{"result":[{"timestamp":[1696253400],"indicators":{"quote":[{"open":[null],'
                            '"low":[null],"high":[null],"close":[null]}],"adjclose":[{"adjclose":[null]}]}}]}}')
        with self.assertRaises(TransformerException):
            HistoricDataTransformer.transform_results(none_values_json, OutputFormat.DICT)


if __name__ == '__main__':
    unittest.main()
