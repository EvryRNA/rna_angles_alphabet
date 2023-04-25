"""
Unit tests to check the preprocessing
"""
import os
import unittest

from src.utils import get_angle
from src.preprocessing.protein_prep import ProteinPrep
from src.preprocessing.rna_prep import RNAPrep

path = os.path.join("tests", "data")

class ModelTest(unittest.TestCase):

    def test_get_rna_values(self):
        """
        Test the rna preprocessing
        """
        class_prep = RNAPrep()
        class_prep.get_values(f"{path}/test_rna.pdb", "test_rna", path)
        test_array = get_angle(f"{path}/test_rna_values.csv", "rna")
        self.assertEqual([155.462,247.584], [test_array[0][0], test_array[0][1]])


    def test_get_prot_values(self):
        """
        Test the protein preprocessing
        """
        class_prep = ProteinPrep()
        class_prep.get_values(f"{path}/test_prot.pdb", "test_prot", path)
        test_array = get_angle(f"{path}/test_prot_values.csv", "protein")
        self.assertEqual([131.987, 85.955], [test_array[0][0], test_array[0][1]])


if __name__ == "__main__":
    unittest.main()
