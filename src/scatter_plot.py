import random
import argparse

import matplotlib.colors as mcolors
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from scipy import stats
import seaborn as sns


def get_angle():
	angle = []

	data = pd.read_csv("data/angle.csv")
	x = np.array(data.ETA.values)
	y = np.array(data.THETA.values)

	"""
	THRESHOLD
	list_indice = []
	angles = np.array([x, y])
	positions = np.vstack([x.ravel(), y.ravel()])

	values = stats.gaussian_kde(angles, bw_method="scott")
	score = values.logpdf(positions)

	sort = np.sort(score)
	thresh = sort[int(np.floor(len(sort)/5))]

	for i in range(0, len(x)):
		if score[i] >= thresh:
			list_indice.append(i)

	x = np.delete(x, list_indice)
	y = np.delete(y, list_indice)
	
	kde_seaborn(list_indice)
	"""

	for j in range(0, len(x)):
		angle.append([x[j], y[j]])
	
	return np.array(angle)


def raw_angle():
	eta, theta = [], []
	angle = get_angle()

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
	if method == "k" or (method == "h" and nb_clusters <= 7):
		colors = ["k", "r", "g", "b", "y", "m", "c"]

	elif method == "d" or (method == "h" and nb_clusters > 7):
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
	plt.show()

	return


def get_colors(nb):
	colors = ["k"]
	list_colors = mcolors.CSS4_COLORS

	for i in range(1, nb):
		colors.append(random.choice(list(list_colors.keys())))

	return colors


def kde_seaborn(list_indice):
	with open("data/angle.csv", "r") as filin, open("data/angle_cut.csv", "w") as filout:
		indice = -1
		for line in filin:
			if indice == -1 or (indice not in list_indice):
				filout.write(line)
			indice += 1

	data_angle = pd.read_csv("data/angle_cut.csv")	
	sns.kdeplot(data = data_angle, x='ETA', y='THETA', bw_method="scott", fill=False, cmap="rocket_r", levels = 8)

	plt.title("η-θ density")
	plt.xlabel("η (degrees)")
	plt.ylabel("θ (degrees)")
	plt.axis([0, 360, 0, 360])
	plt.xticks(np.arange(0, 361, 36))
	plt.yticks(np.arange(0, 361, 36))
	plt.show()

	return


if __name__ == "__main__":
	parser = argparse.ArgumentParser()
	parser.add_argument(
		'--s',
		action='store_true',
		help="Seaborn kde"
	)
	args = parser.parse_args()
	s = args.s
	
	raw_angle()
