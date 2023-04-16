import numpy as np
from sklearn.cluster import DBSCAN, AgglomerativeClustering, KMeans, MeanShift
from sklearn_som.som import SOM

from src.plot_helper import plot_cluster
from src.utils import get_angle, labels_to_seq, load_model, save_model
from src.clustering_classes.clustering_helper import Clustering

class SklearnClust(Clustering):
	def __init__(
		self,
		temp_dir: str,
		method_name: str,
		init_clusters: int
	):
		self.temp_dir = temp_dir,
		self.method_name = method_name,
		self.init_clusters = init_clusters,
		super().__init__()
		
	def train_model(self, temp_dir: str, method_name: str, mol: str, init_clusters: int):
		x_train = get_angle(f"{temp_dir}/train_values.csv")

		if method_name == "dbscan":
			model = DBSCAN(eps=8, min_samples=12)
		elif method_name == "mean_shift":
			model = MeanShift(bandwidth=None)
		elif method_name == "kmeans":
			model = KMeans(n_clusters=init_clusters, n_init="auto")
		elif method_name == "hierarchical":
			model = AgglomerativeClustering(n_clusters=None, linkage="ward", distance_threshold=2000)
		elif method_name == "som":
			model = SOM(m=2, n=2, dim=2)

		cluster_model = model.fit(x_train)
		labels = cluster_model.fit_predict(x_train)
		nb_clusters = len(np.unique(labels))

		print(f"{method_name} clustering done, number of clusters :", nb_clusters, "\n")

		save_model(f"models/{method_name}_{mol}_model.pickle", cluster_model)
		plot_cluster(x_train, labels + 1, nb_clusters, method_name, mol)

		return f"models/{method_name}_{mol}_model.pickle"
		

	def predict_seq(self, temp_dir: str, model_path: str):
		x_test = get_angle(f"{temp_dir}/test_values.csv")

		predict_model = load_model(model_path)
		labels = list(predict_model.fit_predict(x_test))
		seq = labels_to_seq(labels)
		print(seq)
