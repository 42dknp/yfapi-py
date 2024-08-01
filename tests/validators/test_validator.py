# Copyright 2023 Dominic Kneup.
# Licensed under the MIT License; you can find the LICENSE file in the project's root folder.

import unittest
from datetime import datetime
from parameterized import parameterized
from client.exceptions.APIClientExceptions import ValidatorException
from client.api.validators.validator import Validator

class TestValidator(unittest.TestCase):

    # Test valid URLs
    @parameterized.expand([
        ("http://example.com", True),
        ("https://example.com", True),
        ("https://example.com/path", True),
        ("", False),
        ("invalid_url", False),
    ])
    def test_validURL(self, url, expected):
        if expected:
            self.assertTrue(Validator.valid_url(url))
        else:
            with self.assertRaises(Exception):
                Validator.valid_url(url)

    # Test valid intervals
    @parameterized.expand([
        ("1d", True),
        ("1mo", True),
        ("max", True),
        ("", False),
        ("invalid_interval", False),
    ])
    def test_checkInterval(self, interval, expected):
        if expected:
            self.assertTrue(Validator.check_interval(interval))
        else:
            with self.assertRaises(Exception):
                Validator.check_interval(interval)

    # Test date validation
    @parameterized.expand([
        (datetime(2023, 1, 1), datetime(2023, 1, 10), True),
        (datetime(2023, 1, 10), datetime(2023, 1, 1), False),
    ])
    def test_validateDates(self, start_date, end_date, expected):
        if expected:
            self.assertTrue(Validator.validate_dates(start_date, end_date))
        else:
            with self.assertRaises(Exception):
                Validator.validate_dates(start_date, end_date)

    # Test valid API response
    def test_valid_response(self):
        data = '{"chart":{"result":[1, 2, 3],"error":null}}'
        try:
            Validator.check_response_error(data)
        except ValidatorException:
            self.fail("ValidatorException should not have been raised for a valid response")

    # Test API response with chart error
    def test_chart_error(self):
        data = '{"chart":{"result":null,"error":{"code":"Not Found","description":"No data found, symbol may be delisted"}}}'
        with self.assertRaises(ValidatorException):
            Validator.check_response_error(data)

    # Test API response with quote error
    def test_quote_error(self):
        data = '{"quoteResponse":{"result":[],"error":null}}'
        with self.assertRaises(ValidatorException):
            Validator.check_response_error(data)

    # Test API response with finance error
    def test_finance_error(self):
        data = '{"finance":{"result":[],"error":null}}'
        with self.assertRaises(ValidatorException):
            Validator.check_response_error(data)

if __name__ == '__main__':
    unittest.main()
