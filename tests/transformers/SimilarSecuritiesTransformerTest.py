# Copyright 2023 Dominic Kneup.
# Licensed under the MIT License; you can find the LICENSE file in the project's root folder.
import unittest
from client.api.transformers.similar_securities_transformer import SimilarSecuritiesTransformer


class SimilarSecuritiesTransformerTest(unittest.TestCase):
    def test_transform(self):
        json_data = ('{"finance":{"result":[{"symbol":"AMD","recommendedSymbols":[{"symbol":"NVDA","score":0.279067},'
                     '{"symbol":"TSLA","score":0.191081},{"symbol":"INTC","score":0.189413},{"symbol":"META",'
                     '"score":0.182947},{"symbol":"NFLX","score":0.181781}]}],"error":null}}')
        expected_symbols = ['NVDA', 'TSLA', 'INTC', 'META', 'NFLX']

        actual_symbols = SimilarSecuritiesTransformer.data_transformation(json_data)

        self.assertEqual(expected_symbols, actual_symbols)

    def test_output_raw(self):
        json_data = ('{"finance":{"result":[{"symbol":"AMD","recommendedSymbols":[{"symbol":"NVDA","score":0.279067},'
                     '{"symbol":"TSLA","score":0.191081},{"symbol":"INTC","score":0.189413},{"symbol":"META",'
                     '"score":0.182947},{"symbol":"NFLX","score":0.181781}]}],"error":null}}')
        format_type = "raw"

        actual_result = SimilarSecuritiesTransformer.output(json_data, format_type)

        self.assertEqual(json_data, actual_result)

    def test_output_array(self):
        json_data = ('{"finance":{"result":[{"symbol":"AMD","recommendedSymbols":[{"symbol":"NVDA","score":0.279067},'
                     '{"symbol":"TSLA","score":0.191081},{"symbol":"INTC","score":0.189413},{"symbol":"META",'
                     '"score":0.182947},{"symbol":"NFLX","score":0.181781}]}],"error":null}}')
        format_type = "list"
        expected_symbols = ['NVDA', 'TSLA', 'INTC', 'META', 'NFLX']

        actual_result = SimilarSecuritiesTransformer.output(json_data, format_type)

        self.assertEqual(expected_symbols, actual_result)

    def test_output_invalid_format(self):
        with self.assertRaises(Exception) as context:
            json_data = ('{"finance":{"result":[{"symbol":"AMD","recommendedSymbols":[{"symbol":"NVDA",'
                         '"score":0.279067},{"symbol":"TSLA","score":0.191081},{"symbol":"INTC","score":0.189413},'
                         '{"symbol":"META","score":0.182947},{"symbol":"NFLX","score":0.181781}]}],"error":null}}')
            format_type = "invalid"

            SimilarSecuritiesTransformer.output(json_data, format_type)

        self.assertEqual("Output format invalid", str(context.exception))


if __name__ == '__main__':
    unittest.main()
