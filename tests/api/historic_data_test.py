# Copyright 2023 Dominic Kneup.
# Licensed under the MIT License; you can find the LICENSE file in the project's root folder.
import unittest
from datetime import datetime
from client.api.historic_data import HistoricData


class HistoricDataTest(unittest.TestCase):

    def setUp(self):
        self.historic_data = None

        get_historic_data = HistoricData()
        get_historic_data.output = "raw"

        symbol = "AMD"
        start_date = datetime.now().replace(day=1)
        end_date = datetime.now()

        self.historic_data = get_historic_data.get_historic_data(symbol, start_date, end_date)

    def test_get_historic_data_not_null(self):
        self.assertIsNotNone(self.historic_data)

    def test_get_historical_data_is_string(self):
        self.assertIsInstance(self.historic_data, str)


if __name__ == '__main__':
    unittest.main()
