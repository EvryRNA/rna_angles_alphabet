from sklearn.cluster import AgglomerativeClustering

from scatter_plot import get_angle, plot_cluster



def hierarchical_cluster():
	X = get_angle()
	model = AgglomerativeClustering(n_clusters = None, linkage = "ward", distance_threshold = 2000)
	cluster_h = model.fit(X)
	labels = cluster_h.fit_predict(X)

	print("Hierarchical clustering done, number of clusters :", cluster_h.n_clusters_)
	plot_cluster(X, labels, cluster_h.n_clusters_, "h")

	return


if __name__ == '__main__':
	hierarchical_cluster()