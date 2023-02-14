import os

import matplotlib.pyplot as plt
import numpy as np
import seaborn as sns


def csv_angle():
    """
    Function that takes the angle values found by angle.cpp
            and put them in csv format
    """

    with open("data/result.txt", "r") as filin, open("data/angle.csv", "w") as filout:
        # Writing columns name
        filout.write("ETA,THETA\n")

        # Splitting each line in separate values
        for line in filin:
            values = line.split()

            # If both values eta and theta values are present, writing them in the csv
            if values[0] != "THETA" and values[0] != "NA" and values[1] != "NA":
                filout.write(f"{float(values[1])},{float(values[0])}\n")

    print("CSV file with angles values created")

    return


def density2d(x: np.ndarray, y: np.ndarray):
    """
    Function that plot the KDE of the angle values in 2 dimensions
    :param x, y: array matrices of the eta(x) and theta(y) angle values
    """

    # Plotting the kde values in 2D with two different representations
    fig, axes = plt.subplots(2, figsize=(10, 10))
    sns.kdeplot(x=x, y=y, cmap="rocket_r", fill=True, ax=axes[0])
    sns.histplot(x=x, y=y, cmap="rocket_r", thresh=0.5, bins=70, ax=axes[1])

    axes[0].set_title("KDE density")
    axes[1].set_title("KDE histogram density")
    fig.suptitle("2D density plot", fontsize=20)

    plt.show()

    return


def density3d(x: np.ndarray, y: np.ndarray, z: np.ndarray):
    """
    Function that plot the KDE of the angle values in 3 dimensions
    :param x, y: array matrices of the eta(x) and theta(y) angle values
    :param z: array matrix of the kde score of each point
    """

    # Plotting the kde values in 3D with 'trisurf'
    fig, ax = plt.subplots(figsize=(9, 9), subplot_kw={"projection": "3d"})
    surf = ax.plot_trisurf(x, y, z, cmap=plt.cm.jet)

    plt.title("3D density plot", fontsize=20, loc="left")
    fig.colorbar(surf, ax=ax, cmap=plt.cm.jet, aspect=3)
    ax.view_init(45, -115)

    plt.show()

    return


if __name__ == "__main__":
    if not os.path.isfile("data/angle.csv"):
        csv_angle()
