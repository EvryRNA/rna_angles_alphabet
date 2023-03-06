import numpy as np
import pandas as pd
from scipy import stats


def get_values():
    data = pd.read_csv("data/angle.csv")
    eta = np.array(data.ETA.values)
    theta = np.array(data.THETA.values)

    return eta, theta


def kde_scipy():
    x, y = get_values()

    angles = np.array([x, y])
    positions = np.vstack([x.ravel(), y.ravel()])

    values = stats.gaussian_kde(angles, bw_method="scott")
    score = values.logpdf(positions)

    sort = np.sort(score)
    print(np.size(sort))

    return


if __name__ == "__main__":
    kde_scipy()
