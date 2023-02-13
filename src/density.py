import os

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import seaborn as sns


def recup_angle():
	with open("data/result.txt", "r") as filin, open("data/angle.csv", "w") as filout:
		filout.write("ETA,THETA\n")

		for line in filin:
			values = line.split()

			if values[0] != "THETA" and values[0] != "NA" and values[1] != "NA":
				filout.write(f"{float(values[1])},{float(values[0])}\n")

	return


def density2d():
	data = pd.read_csv("data/angle.csv")
	X = np.array(data.ETA.values)
	Y = np.array(data.THETA.values)

	fig, axes = plt.subplots(2, figsize=(10, 10))
	sns.kdeplot(x=X, y=Y, cmap="rocket_r", fill=True, ax=axes[0])
	sns.histplot(x=X, y=Y, cmap="rocket_r", thresh=0.5, bins=70, ax=axes[1])
	axes[0].set_title("KDE density")
	axes[1].set_title("Histogram density")

	plt.show()

	return


if __name__ == "__main__":
	if not os.path.isfile("data/angle.csv"):
		recup_angle()

	density2d()
	