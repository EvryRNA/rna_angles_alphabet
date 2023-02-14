import argparse
import os

import numpy as np
import pandas as pd
from sklearn.neighbors import KernelDensity

from density_plot import csv_angle, density2d, density3d


def preprocess(dim: int, thresh=None):
    """
    Function that process the data depending on the dimension argument
    :param dim: the number of dimensions of the final plot
    :param thresh: optional threshold to remove high density values
    """

    # Reading the angle values and separate them in two arrays 'x' and 'y'
    angle_list, index = [], []
    data = pd.read_csv("data/angle.csv")
    x = np.array(data.ETA.values)
    y = np.array(data.THETA.values)

    # Creating a specific list to retrieve the kde score for each point
    for i in range(0, len(x)):
        angle_list.append([x[i], y[i]])

    # Retrieving the kde scores in an array 'z'
    kde = KernelDensity(kernel="gaussian", bandwidth=0.5).fit(angle_list)
    score = kde.score_samples(angle_list)
    z = np.array(score)

    # If there is threshold argument, checking superior kde value and deleting them
    if thresh is not None:
        for j in range(0, len(z)):
            if z[j] > thresh:
                index.append(j)

        x = np.delete(x, index)
        y = np.delete(y, index)
        z = np.delete(z, index)

    # If the dimension argument is 2
    if dim == 2:
        density2d(x, y)

    # If the dimension argument is 3
    elif dim == 3:
        density3d(x, y, z)

    else:
        print("The dimension argument is wrong")

    return


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "dimension",
        choices=[2, 3],
        type=int,
        help="see the density plot in 2D or 3D",
    )
    parser.add_argument(
        "-t",
        dest="threshold",
        type=float,
        required=False,
        help="remove the high density values with a float",
    )
    args = parser.parse_args()
    dim = args.dimension
    thresh = args.threshold

    # Check if the file with the angle values already exist
    if not os.path.isfile("data/angle.csv"):
        csv_angle()

    if thresh:
        preprocess(dim, thresh)

    else:
        preprocess(dim)
