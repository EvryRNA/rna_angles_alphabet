"""
Unit tests to check the preprocessing
"""
import os
import unittest

from src.utils.utils import get_angle
from src.preprocessing.preprocess_helper import PreprocessHelper

path = os.path.join("tests", "data")

class ModelTest(unittest.TestCase):

    def test_get_rna_values(self):
        """
        Test the rna preprocessing
        """
        class_prep = PreprocessHelper("rna")
        class_prep.get_values(f"{path}/test_rna.pdb", "preprocess_rna", path)

        test_array = get_angle(f"{path}/preprocess_rna_values.csv", "rna")
        self.assertEqual([156.224,214.245], [test_array[0][0], test_array[0][1]])

        os.remove(f"{path}/preprocess_rna_values.csv")


    def test_get_prot_values(self):
        """
        Test the protein preprocessing
        """
        class_prep = PreprocessHelper("prot")
        class_prep.get_values(f"{path}/test_prot.pdb", "preprocess_prot", path)
        
        test_array = get_angle(f"{path}/preprocess_prot_values.csv", "protein")
        self.assertEqual([234.086,15.301], [test_array[0][0], test_array[0][1]])

        os.remove(f"{path}/preprocess_prot_values.csv")

if __name__ == "__main__":
    unittest.main()
