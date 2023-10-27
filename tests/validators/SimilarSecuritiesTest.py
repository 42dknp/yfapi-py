# Copyright 2023 Dominic Kneup.
# Licensed under the MIT License; you can find the LICENSE file in the project's root folder.

import unittest
import json
from client.api.validators.similar_securities_validator import SimilarSecuritiesValidator


class SimilarSecuritiesValidatorTest(unittest.TestCase):
    def setUp(self):
        """
        Setup Demo data (actual api response) for testing
        """
        data = ('{"finance":{"result":[{"symbol":"AMD","recommendedSymbols":[{"symbol":"NVDA","score":0.279067},'
                '{"symbol":"TSLA","score":0.191081},{"symbol":"INTC","score":0.189413},{"symbol":"META",'
                '"score":0.182947},{"symbol":"NFLX","score":0.181781}]}],"error":null}}')

        # Convert json string to object for further use
        self.data_object = json.loads(data)

    def test_map_data_to_object(self):
        self.assertNotEqual(SimilarSecuritiesValidator.validate_results(self.data_object), False)

    def test_validate_results(self):
        data = self.data_object

        # Test for missing recommendedSymbols
        data_missing_recommended_symbols = dict(data)
        del data_missing_recommended_symbols['finance']['result'][0]['recommendedSymbols']

        with self.assertRaises(Exception) as context:
            SimilarSecuritiesValidator.validate_results(data_missing_recommended_symbols)

        self.assertEqual(str(context.exception), 'Missing recommendedSymbols property')

    def test_validate_symbol(self):
        data = self.data_object

        # Test for missing symbol
        data_missing_symbol = dict(data)
        del data_missing_symbol['finance']['result'][0]['symbol']

        with self.assertRaises(Exception) as context:
            SimilarSecuritiesValidator.validate_results(data_missing_symbol)

        self.assertEqual(str(context.exception), 'Missing symbol property')

    def test_validate_recommended_symbols(self):
        data = self.data_object

        # Test for invalid recommendedSymbols format
        data_invalid_recommended_symbols = dict(data)
        data_invalid_recommended_symbols['finance']['result'][0]['recommendedSymbols'] = 'invalid format'

        with self.assertRaises(Exception) as context:
            SimilarSecuritiesValidator.validate_results(data_invalid_recommended_symbols)

        self.assertEqual(str(context.exception), 'Invalid recommendedSymbols format')


if __name__ == '__main__':
    unittest.main()
