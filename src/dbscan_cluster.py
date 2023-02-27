from sklearn.cluster import DBSCAN
import numpy as np

from scatter_plot import get_angle, plot_cluster


def dbscan_cluster():
	X = get_angle()
	model = DBSCAN(eps=5, min_samples=10)
	cluster_db = model.fit(X)
	labels = cluster_db.fit_predict(X)
	nb_cluster = len(np.unique(labels))

	print("DBSCAN clustering done, number of clusters :", nb_cluster)
	plot_cluster(X, labels+1, nb_cluster, "d")

	return


if __name__ == '__main__':
	 dbscan_cluster()
