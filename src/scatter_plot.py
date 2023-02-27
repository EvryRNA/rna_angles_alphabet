import random

import matplotlib.colors as mcolors
import matplotlib.pyplot as plt
import numpy as np


def get_angle():
    eta, theta, angle = [], [], []

    with open("data/result.txt", "r") as filin:
        for line in filin:
            values = line.split()
            if values[0] != "THETA" and values[0] != "NA" and values[1] != "NA":
                theta.append(float(values[0]))
                eta.append(float(values[1]))

    for i in range(0, len(eta)):
        angle.append([eta[i], theta[i]])

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
        scatter = f"plt.scatter(label{i}[:,0], label{i}[:,1], 0.1, color = '{colors[i]}')"
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


if __name__ == "__main__":
    raw_angle()
