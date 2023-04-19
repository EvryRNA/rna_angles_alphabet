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
		x_train = get_angle(f"{self.temp_dir}/train_values.csv")

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
	
		labels = model.fit_predict(x_train)
		nb_clusters = len(np.unique(labels))

		if method_name == "dbscan":
			labels += 1

		elif method_name == "outlier":
			for i in range(0, len(labels)):
				if labels[i] == -1:
					labels[i] = 0

		print(f"{method_name} clustering done, number of clusters :", nb_clusters, "\n")
		print(f"Model saved in models/{method_name}_{self.mol}_model.pickle", "\n")

		save_model(f"models/{method_name}_{self.mol}_model.pickle", model)
		plot_cluster(x_train, labels, nb_clusters, method_name, self.mol)

		return f"models/{method_name}_{self.mol}_model.pickle"
		

	def predict_seq(self, model_path: str):
		x_test = get_angle(f"{self.temp_dir}/test_values.csv")

		predict_model = load_model(model_path)
		labels = list(predict_model.fit_predict(x_test))
		seq = labels_to_seq(labels)
		print(seq)
