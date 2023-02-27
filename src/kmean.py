from sklearn.cluster import KMeans
from sklearn.cluster import AgglomerativeClustering
from sklearn.cluster import DBSCAN
import numpy as np
import argparse

from scatter_plot import get_angle, plot_cluster


def kmeans_cluster(nb_clusters):
	X = get_angle()
	model = KMeans(n_clusters = nb_clusters, n_init = "auto")
	cluster_kmeans = model.fit(X)
	labels = cluster_kmeans.fit_predict(X)

	print("Kmean clustering done, number of clusters :", nb_clusters)
	plot_cluster(X, labels, nb_clusters, "k")

	return


def hierarchical_cluster():
	X = get_angle()
	model = AgglomerativeClustering(n_clusters = None, linkage = "ward", distance_threshold = 2000)
	cluster_h = model.fit(X)
	labels = cluster_h.fit_predict(X)

	print("Hierarchical clustering done, number of clusters :", cluster_h.n_clusters_)
	plot_cluster(X, labels, cluster_h.n_clusters_, "h")

	return


def dbscan_cluster():
	X = get_angle()
	model = DBSCAN(eps=5, min_samples=10)
	cluster_db = model.fit(X)
	labels = cluster_db.fit_predict(X)
	nb_clusters = len(np.unique(labels))

	print("DBSCAN clustering done, number of clusters :", nb_clusters)
	plot_cluster(X, labels+1, nb_clusters, "d")

	return


if __name__ == '__main__':
	parser = argparse.ArgumentParser()
	parser.add_argument('method', type = str, choices = ["k", "h", "d"], help = "Specify the method of clustering, k=kmean, h=hierarchical, d=dbscan")
	parser.add_argument('-n', type = int, choices = range(2, 7), default = 7, help = "If kmeans is chosen, you can specify the number of clusters, default is 7")
	args = parser.parse_args()
	method = args.method
	nb_clusters = args.n

	if method == "k":
		kmeans_cluster(nb_clusters)

	elif method == "h":
		hierarchical_cluster()

	elif method == "d":
		dbscan_cluster()

	else:
		print("wrong method")