# Copyright 2023 Dominic Kneup.
# Licensed under the MIT License; you can find the LICENSE file in the project's root folder.

import unittest
from datetime import datetime

from client.exceptions.APIClientExceptions import ValidatorException
from client.api.validators.validator import Validator


class ValidatorTests(unittest.TestCase):

    def test_validURL(self):
        self.assertTrue(Validator.valid_url("http://example.com"))
        self.assertTrue(Validator.valid_url("https://example.com"))
        self.assertTrue(Validator.valid_url("https://example.com/path"))
        with self.assertRaises(Exception):
            Validator.valid_url("")
        with self.assertRaises(Exception):
            Validator.valid_url("invalid_url")

    def test_checkInterval(self):
        self.assertTrue(Validator.check_interval("1d"))
        self.assertTrue(Validator.check_interval("1mo"))
        self.assertTrue(Validator.check_interval("max"))
        with self.assertRaises(Exception):
            Validator.check_interval("")
        with self.assertRaises(Exception):
            Validator.check_interval("invalid_interval")

    def test_validateDates(self):
        start_date = datetime(2023, 1, 1)
        end_date = datetime(2023, 1, 10)
        self.assertTrue(Validator.validate_dates(start_date, end_date))
        with self.assertRaises(Exception):
            Validator.validate_dates(end_date, start_date)

    def test_valid_response(self):
        # Test a valid api response
        data = '{"chart":{"result":[1, 2, 3],"error":null}}'
        try:
            Validator.check_response_error(data)
        except ValidatorException:
            self.fail("ValidatorException should not have been raised for a valid response")

    def test_chart_error(self):
        # Test an api response with a chart error
        data = '{"chart":{"result":null,"error":{"code":"Not Found","description":"No data found, symbol may be delisted"}}}'
        with self.assertRaises(ValidatorException):
            Validator.check_response_error(data)

    def test_quote_error(self):
        # Test an api response with a quote error
        data = '{"quoteResponse":{"result":[],"error":null}}'
        with self.assertRaises(ValidatorException):
            Validator.check_response_error(data)

    def test_finance_error(self):
        # Test an api response with a finance error
        data = '{"finance":{"result":[],"error":null}}'
        with self.assertRaises(ValidatorException):
            Validator.check_response_error(data)


if __name__ == '__main__':
    unittest.main()
