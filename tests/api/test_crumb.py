"""
Module: CrumbTest

Copyright 2023 Dominic Kneup.
Licensed under the MIT License; you can find the LICENSE file in the project's root folder.
"""
import unittest
from client.api.crumb import Crumb


class TestCrumb(unittest.TestCase):

    crumb_data = None

    def setUp(self):
        """
        Setup Crumb Test
        """

        crumb_instance = Crumb()

        self.crumb_data = crumb_instance.get_crumb()

    def test_crumb_not_null(self):
        self.assertIsNotNone(self.crumb_data)

    def test_crumb_is_string(self):
        self.assertIsInstance(self.crumb_data, str)


if __name__ == '__main__':
    unittest.main()
