import matplotlib.pyplot as plt
import numpy as np


def recup_angle():
	eta, theta, angles = [], [], []

	with open("data/result.txt", "r") as filin:
		for line in filin:
			values = line.split()
			if values[0] != "THETA" and values[0] != "NA" and values[1] != "NA":
				theta.append(float(values[0]))
				eta.append(float(values[1]))

	for i in range(0, len(eta)):
		angles.append([eta[i], theta[i]])
	
	return(angles)



def plot_angle():
	eta, theta = [], []
	tab_angle = recup_angle()

	for i in range(0, len(tab_angle)):
		eta.append(tab_angle[i][0])
		theta.append(tab_angle[i][1])

	plt.scatter(eta, theta, 1, color = 'k')
	plt.title("η-θ conformational space")
	plt.xlabel("η (degrees)")
	plt.ylabel("θ (degrees)")
	plt.axis([0, 360, 0, 360])
	plt.xticks(np.arange(0, 361, 36))
	plt.yticks(np.arange(0, 361, 36))
	plt.show()

	return


if __name__ == '__main__':
	plot_angle()
