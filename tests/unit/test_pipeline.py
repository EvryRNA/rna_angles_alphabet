"""
Unit tests to check the pipeline
"""
import os
import unittest

from src.clustering.r_clust import RClust
from src.clustering.sklearn_clust import SklearnClust
from src.pipeline import Pipeline

path = os.path.join("tests", "data")


class ModelTest(unittest.TestCase):

    def test_initialize_clustering_model(self):
        """
        Test the clustering class initialization with a method or a model
        """
        class_pipe = Pipeline(None, None, None, None, None, None, False)

        r_class = class_pipe.initialize_clustering_model("mclust", None)
        self.assertEqual(RClust, r_class)

        r_model = class_pipe.initialize_clustering_model(None, "mclust_model.Rds")
        self.assertEqual(RClust, r_model)

        sklearn_class = class_pipe.initialize_clustering_model("kmeans", None)
        self.assertEqual(SklearnClust, sklearn_class)

        sklearn_model = class_pipe.initialize_clustering_model(None, "kmeans.pickle")
        self.assertEqual(SklearnClust, sklearn_model)

        # Test the raise ValueError if nothing is given
        with self.assertRaises(ValueError):
            class_pipe.initialize_clustering_model(None, None)


if __name__ == "__main__":
    unittest.main()
