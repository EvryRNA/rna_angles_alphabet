"""
Unit test to check the preprocessing
"""
import os
import unittest

import numpy as np
from src.utils import get_angle
from src.preprocessing.protein_prep import ProteinPrep
from src.preprocessing.rna_prep import RNAPrep

path = os.path.join("tests", "data")
path_rna = os.path.join("tests", "data", "test_rna.pdb")
path_prot = os.path.join("tests", "data", "test_prot.pdb")

class ModelTest(unittest.TestCase):

    def test_get_rna_values(self):
        """
        Test the rna preprocessing
        """
        class_prep = RNAPrep()
        class_prep.get_values(path_rna, "test_rna", path)


    def test_get_prot_values(self):
        """
        Test the protein preprocessing
        """
        class_prep = ProteinPrep()
        class_prep.get_values(path_prot, "test_prot", path)
        test_array = get_angle(f"{path}/test_prot_values.csv", "protein")
        self.assertEqual([131.987, 85.955], [test_array[0][0], test_array[0][1]])















if __name__ == "__main__":
    unittest.main()
