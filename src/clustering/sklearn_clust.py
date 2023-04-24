import numpy as np
from sklearn.cluster import DBSCAN, AgglomerativeClustering, KMeans, MeanShift
from sklearn.ensemble import IsolationForest
from sklearn_som.som import SOM

from src.clustering.clustering_helper import ClusteringHelper
from src.param_model import ParamModel
from src.plot_helper import plot_cluster
from src.utils import get_angle, labels_to_seq, load_model, save_model


class SklearnClust(ClusteringHelper):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def train_model(self, method_name: str, *args, **kwargs) -> str:
        """
        Select a sklearn method to train a model and save it in pickle format

        Args:
                        :param method_name: the name of the clustering method to use
                        :param temp_dir: the path of the temporary directory
            :param mol: the type of biomolecule, protein or rna
                Returns:
            :return the path where the model is saved in pickle format
        """
        # Get the angle values
        x_train = get_angle(f"{self.temp_dir}/train_values.csv", self.mol)

        # Choose the method and execute it with the parameters found in param_model.py
        if method_name == "dbscan":
            model = DBSCAN(**ParamModel.DBSCAN)
        elif method_name == "mean_shift":
            model = MeanShift(**ParamModel.MeanShift)
        elif method_name == "kmeans":
            model = KMeans(**ParamModel.KMeans)
        elif method_name == "hierarchical":
            model = AgglomerativeClustering(**ParamModel.Hierarchical)
        elif method_name == "outlier":
            model = IsolationForest(**ParamModel.Outlier)
        elif method_name == "som":
            model = SOM(**ParamModel.SOM)

        print(f"\n{method_name} clustering starts for {self.mol} data")

        raw_labels = model.fit_predict(x_train)
        nb_clusters = len(np.unique(raw_labels))

        # Rank the labels by the size of their cluster
        labels = self.rank_labels(raw_labels, "plot")

        print(f"\n{method_name} clustering done, number of clusters :", nb_clusters, "\n")
        print(f"Model saved in models/{method_name}_{self.mol}_model.pickle", "\n")

        # Save the model and plot the clusters
        save_model(f"models/{method_name}_{self.mol}_model.pickle", model)
        plot_cluster(x_train, labels, nb_clusters, method_name, self.mol)

        return f"models/{method_name}_{self.mol}_model.pickle"

    def rank_labels(self, labels, plot=False):
        """
                Ranks the labels of a clustering model by size in descending order

        Args:
                        :param labels: an array of labels
                Returns:
            :return an array where the labels reflect the size of their cluster
        """
        # Get the labels in order depending in their size
        if np.unique(labels)[0] == -1:
            # For methods with the -1 label, remove these values for the count
            modif_labels = np.delete(labels, np.where(labels == -1))
            ranked_clusters = list(np.argsort(np.bincount(modif_labels))[::-1])

        else:
            ranked_clusters = list(np.argsort(np.bincount(labels))[::-1])

        # Replace the labels by their place in the ranking, the -1 doesn't change
        for i in range(0, len(labels)):
            if labels[i] != -1:
                labels[i] = ranked_clusters.index(labels[i])

        # The plot function doesn't work with negative values, so 1 is added to all labels
        if plot and np.unique(labels)[0] == -1:
            labels = labels + 1
        return labels

    def predict_seq(self, model_path: str):
        """
        Load a model, fit the data and print the final sequence

        Args:
                        :param model_path: the path to the saved model to use, in pickle format
                        :param temp_dir: the path of the temporary directory
                        :param mol: the type of biomolecule, protein or rna
        """
        # Get the angle values to fit on the model
        x_test = get_angle(f"{self.temp_dir}/test_values.csv", self.mol)

        # Fit the data, get the labels and rank them with rank_labels
        predict_model = load_model(model_path)
        raw_labels = predict_model.fit_predict(x_test)
        labels = self.rank_labels(raw_labels)

        # Use the labels to compute and print the corresponding sequence
        seq = labels_to_seq(labels)
        print(seq)
