# Copyright 2023 Dominic Kneup.
# Licensed under the MIT License; you can find the LICENSE file in the project's root folder.

import unittest
from client.api.similar_securities import SimilarSecurities  


class TestSimilarSecurities(unittest.TestCase):
    def setUp(self):
        
        get_similar_securities = SimilarSecurities()
        get_similar_securities.output_format = "raw"
        symbol = "GS"
        
        self.similar_securities_data = get_similar_securities.get_similar_securities(symbol)

    def test_similar_securities_not_none(self):
        self.assertIsNotNone(self.similar_securities_data)

    def test_similar_securities_is_string(self):
        self.assertIsInstance(self.similar_securities_data, str)


if __name__ == '__main__':
    unittest.main()
