from sklearn.cluster import AgglomerativeClustering
import matplotlib.pyplot as plt
import numpy as np
import random



def recup_angle():
	eta, theta, list_angle = [], [], []

	with open("result.txt", "r") as filin:
		for line in filin:
			values = line.split()
			if values[0] != "THETA" and values[0] != "NA" and values[1] != "NA":
				theta.append(float(values[0]))
				eta.append(float(values[1]))

	for i in range(0, len(eta)):
		list_angle.append([eta[i], theta[i]])

	hierarchical(list_angle)



def hierarchical(list_angle):
	X = np.array(list_angle)
	agglo = AgglomerativeClustering(n_clusters = None, linkage = "ward", distance_threshold = 2000).fit(X)
	labels = agglo.fit_predict(X)

	print("Clustering done, number of clusters :", agglo.n_clusters_)
	plot_cluster(X, labels, agglo.n_clusters_)



def plot_cluster(data, label, nb_clusters):
	colors = ["b", "g", "m", "k", "y", "c", "r"]

	for i in range(0,nb_clusters):
		filter = f"label{i} = data[label == {i}]"
		exec(filter)
		rand_c = random.choice(colors)
		colors.remove(rand_c)
		scatter = f"plt.scatter(label{i}[:,0], label{i}[:,1], 0.5, color = '{rand_c}')"
		exec(scatter)

	plt.title("η-θ conformational space")
	plt.xlabel("η (degrees)")
	plt.ylabel("θ (degrees)")
	plt.axis([0, 360, 0, 360])
	plt.xticks(np.arange(0, 361, 36))
	plt.yticks(np.arange(0, 361, 36))
	plt.show()




if __name__ == '__main__':
	recup_angle()
