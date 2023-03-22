import random

import matplotlib.colors as mcolors
import matplotlib.pyplot as plt
import numpy as np

from src.utils import get_angle


def raw_angle(path):
	"""
	Plot the raw data of angle values using a csv file
	"""
	eta, theta = [], []
	angle = get_angle(path)

	for i in range(0, len(angle)):
		eta.append(angle[i][0])
		theta.append(angle[i][1])

	plt.scatter(eta, theta, 1, color="k")
	plt.title("η-θ conformational space")
	plt.xlabel("η (degrees)")
	plt.ylabel("θ (degrees)")
	plt.axis([0, 360, 0, 360])
	plt.xticks(np.arange(0, 361, 36))
	plt.yticks(np.arange(0, 361, 36))
	plt.show()

	return


def plot_cluster(data, label, nb_clusters, method):
	"""
	Plot the results of a clustering method
	"""
	if nb_clusters <= 7:
		colors = ["k", "r", "g", "b", "y", "m", "c"]

	elif nb_clusters > 7:
		colors = get_colors(nb_clusters)

	for i in range(0, nb_clusters):
		filter = f"label{i} = data[label == {i}]"
		exec(filter)
		scatter = f"plt.scatter(label{i}[:,0], label{i}[:,1], 2, color = '{colors[i]}')"
		exec(scatter)

	plt.title("η-θ conformational space")
	plt.xlabel("η (degrees)")
	plt.ylabel("θ (degrees)")
	plt.axis([0, 360, 0, 360])
	plt.xticks(np.arange(0, 361, 36))
	plt.yticks(np.arange(0, 361, 36))
	plt.savefig(f"tmp/{method}_cluster.png")

	return


def get_colors(nb):
	"""
	Return a list of random colors
	"""
	colors = ["k"]
	list_colors = mcolors.CSS4_COLORS

	for i in range(1, nb):
		colors.append(random.choice(list(list_colors.keys())))

	return colors


if __name__ == "__main__":	
	raw_angle("tmp/result_train.csv")
