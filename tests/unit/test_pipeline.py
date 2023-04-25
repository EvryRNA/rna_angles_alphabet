"""
Unit tests to check the pipeline
"""
import os
import unittest

from src.pipeline import Pipeline

path = os.path.join("tests", "data", "test_unit.txt")


class ModelTest(unittest.TestCase):
    
    def test_preprocess_data(self):
        """
        Test the data preprocessing
        """
        class_pipe = Pipeline("tests/data/test_rna_values.csv", "tests/data/test_rna_values.csv", "tests/data", "dbscan", "rna", None, False)
        class_pipe.preprocess_data("tests/data", "tests/data/test_rna_values.csv",
                                   "tests/data/test_rna_values.csv", "rna", "test")


if __name__ == "__main__":
    unittest.main()
