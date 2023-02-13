import unittest

import numpy as np

import os

from src.density import recup_angle

from src.code_example import sum_image


class SumTest(unittest.TestCase):
    def test_sum(self):
        inputs = np.array([[0, 1], [3, 0]])
        expected_sum = 4
        predicted_sum = sum_image(inputs)
        self.assertTrue(expected_sum == predicted_sum)

    def test_csv(self):
        if not os.path.isfile("data/angle.csv"):
            recup_angle()
            self.assertTrue(os.path.isfile("data/angle.csv"))



if __name__ == "__main__":
    unittest.main()
