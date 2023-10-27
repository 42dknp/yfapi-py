# Copyright 2023 Dominic Kneup.
# Licensed under the MIT License; you can find the LICENSE file in the project's root folder.

import unittest
from client.api.validators.crumb_validator import CrumbValidator


class CrumbValidatorTest(unittest.TestCase):

    # Test if method returns the value that was sent
    def testValidCrumbSymbols(self):
        # Test case 1: input has numbers, letters, and symbols
        input1 = "abc123@#$"
        self.assertEqual(input1, CrumbValidator.validate_crumb(input1))

    # Test if Exception is raised correctly
    def testValidateCrumbReturnsErrorMessageWhenEmpty(self):
        # Arrange
        crumb = ''
        with self.assertRaises(Exception):
            # Act
            CrumbValidator.validate_crumb(crumb)

