# Copyright 2023 Dominic Kneup.
# Licensed under the MIT License; you can find the LICENSE file in the project's root folder.
import unittest
from parameterized import parameterized
from client.api.transformers.similar_securities_transformer import SimilarSecuritiesTransformer, OutputFormat
from client.exceptions import APIClientExceptions

class TestSimilarSecuritiesTransformer(unittest.TestCase):

    @parameterized.expand([
        # Valid JSON data with multiple recommended symbols
        ('{"finance":{"result":[{"symbol":"AMD","recommendedSymbols":[{"symbol":"NVDA","score":0.279067},'
         '{"symbol":"TSLA","score":0.191081},{"symbol":"INTC","score":0.189413},{"symbol":"META",'
         '"score":0.182947},{"symbol":"NFLX","score":0.181781}]}],"error":null}}',
         ['NVDA', 'TSLA', 'INTC', 'META', 'NFLX']),

        # Valid JSON data with no recommended symbols
        ('{"finance":{"result":[{"symbol":"AMD","recommendedSymbols":[]}],"error":null}}',
         []),
         
        # Valid JSON data with a single recommended symbol
        ('{"finance":{"result":[{"symbol":"AMD","recommendedSymbols":[{"symbol":"NVDA","score":0.279067}]}],"error":null}}',
         ['NVDA']),

        # Valid JSON data with error field set
        ('{"finance":{"result":[{"symbol":"AMD","recommendedSymbols":[{"symbol":"NVDA","score":0.279067}]}],"error":"Some error"}}',
         ['NVDA'])
    ])
    
    def test_transform(self, json_data, expected_symbols):
        actual_symbols = SimilarSecuritiesTransformer.data_transformation(json_data)
        self.assertEqual(expected_symbols, actual_symbols)

    @parameterized.expand([
        # Valid JSON data with multiple recommended symbols
        ('{"finance":{"result":[{"symbol":"AMD","recommendedSymbols":[{"symbol":"NVDA","score":0.279067},'
         '{"symbol":"TSLA","score":0.191081},{"symbol":"INTC","score":0.189413},{"symbol":"META",'
         '"score":0.182947},{"symbol":"NFLX","score":0.181781}]}],"error":null}}', OutputFormat.RAW),
        
        # Valid JSON data with no recommended symbols
        ('{"finance":{"result":[{"symbol":"AMD","recommendedSymbols":[]}],"error":null}}', OutputFormat.RAW)
    ])

    def test_output_raw(self, json_data, format_type):
        actual_result = SimilarSecuritiesTransformer.output(json_data, format_type)
        self.assertEqual(json_data, actual_result)

    @parameterized.expand([
        # Valid JSON data with multiple recommended symbols
        ('{"finance":{"result":[{"symbol":"AMD","recommendedSymbols":[{"symbol":"NVDA","score":0.279067},'
         '{"symbol":"TSLA","score":0.191081},{"symbol":"INTC","score":0.189413},{"symbol":"META",'
         '"score":0.182947},{"symbol":"NFLX","score":0.181781}]}],"error":null}}', OutputFormat.LIST,
         ['NVDA', 'TSLA', 'INTC', 'META', 'NFLX']),
        
        # Valid JSON data with no recommended symbols
        ('{"finance":{"result":[{"symbol":"AMD","recommendedSymbols":[]}],"error":null}}', OutputFormat.LIST,
         []),
        
        # Valid JSON data with a single recommended symbol
        ('{"finance":{"result":[{"symbol":"AMD","recommendedSymbols":[{"symbol":"NVDA","score":0.279067}]}],"error":null}}', OutputFormat.LIST,
         ['NVDA'])
    ])

    def test_output_array(self, json_data, format_type, expected_symbols):
        actual_result = SimilarSecuritiesTransformer.output(json_data, format_type)
        self.assertEqual(expected_symbols, actual_result)

if __name__ == '__main__':
    unittest.main()

