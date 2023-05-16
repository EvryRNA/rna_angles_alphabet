import matplotlib.pyplot as plt
import numpy as np

from src.utils.utils import get_angle, get_colors


def raw_data_plot(path: str, mol: str):
    """
    Plot the raw data of angle values using a csv file

    Args:
        :param path: the name of the csv containing the angle values
        :param mol: the type of biomolecule, protein or rna
    """
    x_values, y_values = [], []
    angle_values = get_angle(path, mol)

    # Separate the x and y values in 2 distinct lists
    for i in range(0, len(angle_values)):
        x_values.append(angle_values[i][0])
        y_values.append(angle_values[i][1])

    # Choose the axis names depending on the type of molecule
    if mol == "rna":
        angle_names = ["η", "θ"]
    elif mol == "protein":
        angle_names = ["φ", "ψ"]
    else:
        print("\nWrong molecule type given\n")

    plt.scatter(x_values, y_values, 1, color="k")
    plt.title(f"{angle_names[0]}-{angle_names[1]} conformational space")
    plt.xlabel(f"{angle_names[0]} (degrees)")
    plt.ylabel(f"{angle_names[1]} (degrees)")
    plt.axis([0, 360, 0, 360])
    plt.xticks(np.arange(0, 361, 36))
    plt.yticks(np.arange(0, 361, 36))
    plt.savefig(f"figures_clust/raw_{mol}_data.png")

    print(f"\nRaw data saved in figures_clust/raw_{mol}_data.png\n")


def plot_cluster(x, label: list, nb_clusters: int, method: str, mol: str):
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
    # Give as many colors as the number of clusters
    colors = get_colors(nb_clusters)

    # Add each cluster to the plot one by one
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
    plt.savefig(f"figures_clust/{method}_{mol}_cluster.png")

    print(f"Clustering saved in figures_clust/{method}_{mol}_cluster.png\n")
