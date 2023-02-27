from sklearn.cluster import DBSCAN
import numpy as np
import random
import matplotlib.pyplot as plt
import matplotlib.colors as mcolors


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

	dbscan(list_angle)

	return


def dbscan(list_angle):
	angles = np.array(list_angle)
	model = DBSCAN(eps=5, min_samples=10)
	cluster = model.fit(angles)
	labels = cluster.fit_predict(angles)

	print("DBSCAN clustering done, number of clusters :", len(np.unique(labels)))
	plot_cluster(angles, labels+1)

	return


def plot_cluster(data, label):
	colors = mcolors.CSS4_COLORS
	nb_cluster = len(np.unique(label))

	for i in range(0, nb_cluster):
		filter = f"label{i} = data[label == {i}]"
		exec(filter)
		if i == 0:
			scatter = f"plt.scatter(label{i}[:,0], label{i}[:,1], 2, color = 'w')"
			exec(scatter)
		else:
			c = random.choice(list(colors.keys()))
			scatter = f"plt.scatter(label{i}[:,0], label{i}[:,1], 2, color = '{colors[c]}')"
			exec(scatter)

	plt.title("η-θ conformational space")
	plt.xlabel("η (degrees)")
	plt.ylabel("θ (degrees)")
	plt.axis([0, 360, 0, 360])
	plt.xticks(np.arange(0, 361, 36))
	plt.yticks(np.arange(0, 361, 36))
	print("DBscan clustering done")
	plt.show()


if __name__ == '__main__':
	 recup_angle()
