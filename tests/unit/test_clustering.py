"""
Unit tests to check the custering
"""
import numpy as np
import os
import unittest

import sys
from io import StringIO 

from src.utils import get_angle
from src.clustering.sklearn_clust import SklearnClust
from src.clustering.r_clust import RClust
from src.pipeline import Pipeline

path = os.path.join("tests", "data")

class ModelTest(unittest.TestCase):

    def test_mclust_clustering(self):
        """
        Test the R clustering
        """
        class_cluster = RClust(path, "rna")

        model = class_cluster.train_model()
        self.assertEqual("models/mclust_rna_model.Rds", model)

    
    def test_rank_labels(self):
        """
        Test the labels ranking
        """
        class_cluster = SklearnClust(path, "rna")

        labels = class_cluster.rank_labels(np.array([-1, 2, 1, 1, 1, -1, 0, 2]))
        self.assertEqual([-1, 1, 0, 0, 0, -1, 2, 1], list(labels))

        labels = class_cluster.rank_labels(np.array([-1, 2, 1, 1, 1, -1, 0, 2]), "plot")
        self.assertEqual([0, 2, 1, 1, 1, 0, 3, 2], list(labels))


    def test_predict_seq(self):
        """
        Test the sequence predict
        """
        class_cluster = SklearnClust(path, "rna")
        class_pipe = Pipeline(None, None, path, None, "rna", None, False)
        class_pipe.preprocess_data(f"{path}/test_rna.pdb", f"{path}/test_rna.pdb")

        capturedOutput = StringIO()
        sys.stdout = capturedOutput
        class_cluster.predict_seq("tests/data/test_dbscan_rna_model.pickle",
                                  np.array([[1, 2], [3, 4]]))
        sys.stdout = sys.__stdout__

        self.assertEqual("--\n", capturedOutput.getvalue())


        

if __name__ == "__main__":
    unittest.main()
