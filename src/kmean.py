from sklearn.cluster import KMeans
import argparse

from scatter_plot import get_angle, plot_cluster


def kmeans_cluster():
	X = get_angle()
	model = KMeans(n_clusters = nb_clusters, n_init = "auto")
	cluster_kmeans = model.fit(X)
	labels = cluster_kmeans.fit_predict(X)

	print("Kmean clustering done")
	plot_cluster(X, labels, nb_clusters, "k")

	return


if __name__ == '__main__':
	parser = argparse.ArgumentParser()
	parser.add_argument('n', type = int, choices = range(2, 8), help = "Specify the number of clusters")
	args = parser.parse_args()
	nb_clusters = args.n

	kmeans_cluster()