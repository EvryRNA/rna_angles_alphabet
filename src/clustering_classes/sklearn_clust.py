import numpy as np
from sklearn.cluster import DBSCAN, AgglomerativeClustering, KMeans, MeanShift
from sklearn_som.som import SOM
from sklearn.ensemble import IsolationForest
from src.param_model import ParamModel

from src.plot_helper import plot_cluster
from src.utils import get_angle, labels_to_seq, load_model, save_model
from src.clustering_classes.clustering_helper import Clustering

class SklearnClust(Clustering):
	def __init__(self, *args, **kwargs):
		super().__init__(*args, **kwargs)
		
	def train_model(self, method_name: str,*args, **kwargs)-> str:
		x_train = get_angle(f"{self.temp_dir}/train_values.csv", self.mol)

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

		labels = self.order_labels(raw_labels)

		print(f"\n{method_name} clustering done, number of clusters :", nb_clusters, "\n")
		print(f"Model saved in models/{method_name}_{self.mol}_model.pickle", "\n")

		save_model(f"models/{method_name}_{self.mol}_model.pickle", model)
		plot_cluster(x_train, labels, nb_clusters, method_name, self.mol)

		return f"models/{method_name}_{self.mol}_model.pickle"
		

	def order_labels(self, raw_labels):

		final_labels = raw_labels
		
		if np.unique(raw_labels)[0] == -1:
			modif_labels = np.delete(raw_labels, np.where(raw_labels == -1))
			ordered_clusters = list(np.argsort(np.bincount(modif_labels))[::-1])

		else:
			ordered_clusters = list(np.argsort(np.bincount(raw_labels))[::-1])

		for i in range(0, len(final_labels)):
			if final_labels[i] != -1:
				final_labels[i] = ordered_clusters.index(final_labels[i])

		if np.unique(raw_labels)[0] == -1:
			final_labels = final_labels + 1

		return(final_labels)


	def predict_seq(self, model_path: str):
		x_test = get_angle(f"{self.temp_dir}/test_values.csv", self.mol)

		predict_model = load_model(model_path)
		labels = list(predict_model.fit_predict(x_test))
		seq = labels_to_seq(labels)
		print(seq)
