import unittest

import numpy as np

from src.code_example import sum_image


class SumTest(unittest.TestCase):
    def test_sum(self):
        inputs = np.array([[0, 1], [3, 0]])
        expected_sum = 4
        predicted_sum = sum_image(inputs)
        self.assertTrue(expected_sum == predicted_sum)



if __name__ == "__main__":
    unittest.main()
