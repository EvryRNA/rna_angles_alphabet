from sklearn.cluster import KMeans
import matplotlib.pyplot as plt
import numpy as np
import argparse
import random


def recup_angle():
	eta, theta, list_angle = [], [], []

	with open("data/result.txt", "r") as filin:
		for line in filin:
			values = line.split()
			if values[0] != "THETA" and values[0] != "NA" and values[1] != "NA":
				theta.append(float(values[0]))
				eta.append(float(values[1]))

	for i in range(0, len(eta)):
		list_angle.append([eta[i], theta[i]])

	cluster_kmeans(list_angle)

	return

		
def cluster_kmeans(list_angle):
	X = np.array(list_angle)
	cluster_model = KMeans(n_clusters = nb_clusters, n_init = "auto")
	kmeans = cluster_model.fit(X)
	labels = kmeans.fit_predict(X)

	print("Kmean clustering done")
	plot_cluster(X, labels)

	return


def plot_cluster(data, label):
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

	return



if __name__ == '__main__':
	parser = argparse.ArgumentParser()
	parser.add_argument('n', type = int, choices = range(2, 8), help = "Specify the number of clusters")
	args = parser.parse_args()
	nb_clusters = args.n

	recup_angle()