from sklearn.cluster import DBSCAN
import numpy as np
import random
import matplotlib.pyplot as plt
import matplotlib.colors as mcolors

from process_density import preprocess


def dbscan():
	x, y = preprocess()
	angles = np.empty((len(x), 2))

	for i in range(0, len(x)):
		angles[i,0] = x[i]
		angles[i,1] = y[i] 

	model = DBSCAN(eps=5, min_samples=8)
	cluster = model.fit(angles)
	labels = cluster.fit_predict(angles)

	plot_cluster(angles, labels+1)


def plot_cluster(data, label):
	colors = mcolors.CSS4_COLORS
	nb_cluster = len(np.unique(label))

	for i in range(0, nb_cluster):
		filter = f"label{i} = data[label == {i}]"
		exec(filter)
		if i == 0:
			scatter = f"plt.scatter(label{i}[:,0], label{i}[:,1], 1, color = 'w')"
			exec(scatter)
		else:
			c = random.choice(list(colors.keys()))
			scatter = f"plt.scatter(label{i}[:,0], label{i}[:,1], 1, color = '{colors[c]}')"
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
	 dbscan()
