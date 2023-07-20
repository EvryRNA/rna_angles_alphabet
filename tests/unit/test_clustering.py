"""
Unit tests to check the clustering
"""
import numpy as np
import os
import unittest

from src.utils.utils import labels_to_seq
from src.clustering.sklearn_clust import SklearnClust
from src.clustering.r_clust import RClust

path = os.path.join("tests", "data")

class ModelTest(unittest.TestCase):

    def test_mclust_clustering(self):
        """
        Test the R clustering
        """
        class_cluster = RClust(path, "rna", "mclust")

        model = class_cluster.train_model()
        self.assertEqual("models/mclust_rna_model.Rds", model)

    
    def test_sklearn_clustering(self):
        """
        Test the sequence predict for each method
        """
        x_train = np.array([[1, 1], [2, 2], [8, 8], [9, 9], [50, 50]])
        x_test = np.array([[1, 2], [7, 8], [2, 3], [0, 1], [50, 50], [8, 9]])

        ### For KMeans
        class_cluster = SklearnClust(path, "rna", "kmeans")
        path_model = class_cluster.train_model("kmeans", x_train, dict(n_clusters=3))
        final_seq = "ABAACB"

        test_seq = class_cluster.predict_seq(path_model, x_test)
        self.assertEqual(final_seq, test_seq)

        ### For Mean_Shift
        class_cluster = SklearnClust(path, "rna", "mean_shift")
        path_model = class_cluster.train_model("mean_shift", x_train, dict(bandwidth=2))
        final_seq = "ABAACB"

        test_seq = class_cluster.predict_seq(path_model, x_test)
        self.assertEqual(final_seq, test_seq)
        
        ### For default Outlier
        class_cluster = SklearnClust(path, "rna", "outlier")
        path_model = class_cluster.train_model("outlier", x_train)
        final_seq = "AAAA-A"

        test_seq = class_cluster.predict_seq(path_model, x_test)
        self.assertEqual(final_seq, test_seq)

        
    def test_rank_labels(self): 
        """
        Test the labels ranking
        """
        class_cluster = SklearnClust(path, "rna", "mean_shift")

        labels = class_cluster.rank_labels(np.array([-1, 1, 0, 1]))
        self.assertEqual([-1, 0, 1, 0], list(labels))

        labels = class_cluster.rank_labels(np.array([-1, 1, 0, 1]), "plot")
        self.assertEqual([0, 1, 2, 1], list(labels))


    def test_labels_to_seq(self):
        """
        Test the labels to seq function
        """
        test_labels = [-1, 0, 1, 3, -1, 2, 3, 0, -1,]
        self.assertEqual("-ABD-CDA-", labels_to_seq(test_labels))    


if __name__ == "__main__":
    unittest.main()
