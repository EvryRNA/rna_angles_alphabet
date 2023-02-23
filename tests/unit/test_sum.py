import unittest

import os

from src.density_plot import csv_angle


class SumTest(unittest.TestCase):
    def test_csv(self):
        if not os.path.isfile("data/angle.csv"):
            csv_angle()
            self.assertTrue(os.path.isfile("data/angle.csv"))



if __name__ == "__main__":
    unittest.main()
