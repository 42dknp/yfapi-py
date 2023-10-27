# Copyright 2023 Dominic Kneup.
# Licensed under the MIT License; you can find the LICENSE file in the project's root folder.

import unittest
from client.api.quote import Quote


class QuoteTest(unittest.TestCase):
    def setUp(self):
        super().setUp()

        self.getQuote = Quote()
        self.getQuote.output = "raw"  # Set output format to raw (json text string)

        self.symbol = "TSM"

        # Get a new Crumb
        self.quote_data = self.getQuote.get_quote(self.symbol)

    def test_quote_not_null(self):
        self.assertIsNotNone(self.quote_data)

    def test_quote_is_string(self):
        self.assertIsInstance(self.quote_data, str)
