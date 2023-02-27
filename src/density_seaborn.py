import seaborn as sns
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt


def density_plot():
    X = pd.read_csv("data/angle.csv")
    sns.kdeplot(data=X, x="ETA", y="THETA", bw_method="scott", fill=True, cmap="rocket_r", thresh=0.1)

    plt.title("η-θ density")
    plt.xlabel("η (degrees)")
    plt.ylabel("θ (degrees)")
    plt.axis([0, 360, 0, 360])
    plt.xticks(np.arange(0, 361, 36))
    plt.yticks(np.arange(0, 361, 36))
    plt.show()

    return


if __name__ == "__main__":
    density_plot()
