"""
Unit tests to check the pipeline
"""
import os
import unittest

from src.clustering.r_clust import RClust
from src.clustering.sklearn_clust import SklearnClust
from src.pipeline import Pipeline
from src.utils import get_angle

path = os.path.join("tests", "data")


class ModelTest(unittest.TestCase):
    
    def test_preprocess_data(self):
        """
        Test the data preprocessing
        """
        class_pipe = Pipeline(None, None, path, None, "rna", None, False)
        class_pipe.preprocess_data(f"{path}/test_rna.pdb", f"{path}/test_rna.pdb")

        test_array = get_angle(f"{path}/test_values.csv", "rna")
        self.assertEqual([156.224,214.245], [test_array[0][0], test_array[0][1]])

        train_array = get_angle(f"{path}/train_values.csv", "rna")
        self.assertEqual([156.224,214.245], [train_array[0][0], train_array[0][1]])

        os.remove(f"{path}/test_values.csv")
        os.remove(f"{path}/train_values.csv")


    def test_initialize_clustering_model(self):
        """
        Test the clustering class initialization with a method or a model
        """
        class_pipe = Pipeline(None, None, None, None, None, None, False)

        r_class = class_pipe.initialize_clustering_model("mclust", None)
        self.assertEqual(RClust, r_class)

        r_model = class_pipe.initialize_clustering_model(None, "mclust_model.Rds")
        self.assertEqual(RClust, r_model)

        sklearn_class = class_pipe.initialize_clustering_model("dbscan", None)
        self.assertEqual(SklearnClust, sklearn_class)

        sklearn_model = class_pipe.initialize_clustering_model(None, "dbscan.pickle")
        self.assertEqual(SklearnClust, sklearn_model)

        # Test the raise ValueError if nothing is given
        with self.assertRaises(ValueError):
            class_pipe.initialize_clustering_model(None, None)


if __name__ == "__main__":
    unittest.main()
