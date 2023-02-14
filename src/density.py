import argparse
import os

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import seaborn as sns
from sklearn.neighbors import KernelDensity


def recup_angle():
    with open("data/result.txt", "r") as filin, open("data/angle.csv", "w") as filout:
        filout.write("ETA,THETA\n")

        for line in filin:
            values = line.split()

            if values[0] != "THETA" and values[0] != "NA" and values[1] != "NA":
                filout.write(f"{float(values[1])},{float(values[0])}\n")
    print("CSV file with angles values created")

    return


def preprocess(dim):
    data  = pd.read_csv("data/angle.csv")
    x = np.array(data.ETA.values)
    y = np.array(data.THETA.values)
    
    if dim == 2:
        density2d(x, y)

    elif dim == 3:
        angle_list= []
        
        for i in range(0, len(x)):
            angle_list.append([x[i], y[i]])

        kde = KernelDensity(kernel="gaussian", bandwidth=0.5).fit(angle_list)
        score = kde.score_samples(angle_list)
        z = np.array(score)
        density3d(x, y, z)

    else:
        print("The dimension argument is wrong")
    
    return


def density2d(x, y):
    fig, axes = plt.subplots(2, figsize=(10, 10))
    sns.kdeplot(x=x, y=y, cmap="rocket_r", fill=True, ax=axes[0])
    sns.histplot(x=x, y=y, cmap="rocket_r", thresh=0.5, bins=70, ax=axes[1])

    axes[0].set_title("KDE density")
    axes[1].set_title("Histogram density")
    fig.suptitle("2D density plot", fontsize=20)

    plt.show()

    return


def density3d(x, y, z):
    fig, ax = plt.subplots(figsize=(9, 9), subplot_kw={"projection": "3d"})
    surf = ax.plot_trisurf(x, y, z, cmap=plt.cm.jet)
    plt.title("3D density plot", fontsize=20, loc="left")
    ax.view_init(45, -115)
    fig.colorbar(surf, ax=ax, cmap=plt.cm.jet, aspect=3)

    plt.show()

    return


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "-d",
        choices=[2, 3],
        required=True,
        type=int,
        action="store",
        help="See the density plot in 2d or 3d",
    )
    args = parser.parse_args()
    dim = args.d

    if not os.path.isfile("data/angle.csv"):
        recup_angle()

    preprocess(dim)
