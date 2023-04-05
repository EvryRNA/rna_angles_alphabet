import random

import matplotlib.colors as mcolors
import matplotlib.pyplot as plt
import numpy as np

from src.utils import get_angle


def raw_angle(path: str):
    """
    Plot the raw data of angle values using a csv file

    Args:
        :param path: the name of the csv containing the angle values
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
    plt.savefig("raw_data.png")


def plot_cluster(x, label: list, nb_clusters: int, method: str, temp_dir: str):
    """
    Plot the results of a clustering method

    Args:
        :param x: a np.array of size (N, M) with N the number of couples of angles of the
                training set and M their values
        :param label: list of the labels of the model
        :param nb_clusters: number of clusters of the model
        :param method: name of the clustering method used
        :param temp_dir: the path of the temporary directory
    """
    if nb_clusters <= 7:
        colors = ["k", "r", "g", "b", "y", "m", "c"]

    elif nb_clusters > 7:
        colors = get_colors(nb_clusters)

    for i in range(0, nb_clusters):
        filter = f"label{i} = x[label == {i}]"
        exec(filter)
        scatter = f"plt.scatter(label{i}[:,0], label{i}[:,1], 2, color = '{colors[i]}')"
        exec(scatter)

    plt.title("η-θ conformational space")
    plt.xlabel("η (degrees)")
    plt.ylabel("θ (degrees)")
    plt.axis([0, 360, 0, 360])
    plt.xticks(np.arange(0, 361, 36))
    plt.yticks(np.arange(0, 361, 36))
    plt.savefig(f"{temp_dir}/{method}_cluster.png")

    print(f"Clustering save: {temp_dir}/{method}_cluster.png\n")


def get_colors(nb_colors: int):
    """
    Return a list of random colors

    Args:
        :param nb_colors: the number of colors to return
    """
    colors = ["k"]
    list_colors = mcolors.CSS4_COLORS

    for i in range(1, nb_colors):
        colors.append(random.choice(list(list_colors.keys())))

    return colors
