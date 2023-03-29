import argparse
from typing import Any

import numpy as np
from sklearn.cluster import DBSCAN, AgglomerativeClustering, KMeans, MeanShift

from src.scatter_plot import plot_cluster
from src.utils import load_model, save_model


def kmeans_cluster(x: np.array, nb_clusters: int, temp_dir: str):
    """
    Train a kmeans model on a dataset
    """
    model = KMeans(n_clusters=nb_clusters, n_init="auto")
    cluster_kmeans = model.fit(x)
    labels = cluster_kmeans.fit_predict(x)

    print("Kmean clustering done, number of clusters :", nb_clusters)

    save_model(f"{temp_dir}/kmeans_model.pickle", cluster_kmeans)
    plot_cluster(x, labels, nb_clusters, "kmeans", temp_dir)

    return


def hierarchical_cluster(x: np.array, temp_dir: str):
    """
    Train a hierarchical model on a dataset
    """
    model = AgglomerativeClustering(n_clusters=None, linkage="ward", distance_threshold=2000)
    cluster_h = model.fit(x)
    labels = cluster_h.fit_predict(x)

    print("Hierarchical clustering done, number of clusters :", cluster_h.n_clusters_)

    save_model(f"{temp_dir}/hierarchical_model.pickle", cluster_h)
    plot_cluster(x, labels, cluster_h.n_clusters_, "hierarchical", temp_dir)

    return


def dbscan_cluster(x: np.array, temp_dir: str):
    """
    Train a dbscan model on a dataset
    """
    model = DBSCAN(eps=8, min_samples=12)
    cluster_db = model.fit(x)
    labels = cluster_db.fit_predict(x)
    nb_clusters = len(np.unique(labels))

    print("DBSCAN clustering done, number of clusters :", nb_clusters)

    save_model(f"{temp_dir}/dbscan_model.pickle", cluster_db)
    plot_cluster(x, labels + 1, nb_clusters, "dbscan", temp_dir)

    return


def mean_shift_cluster(x: np.array, temp_dir: str):
    """
    Train a mean shift model on a dataset
    """
    model = MeanShift(bandwidth=None)
    cluster_ms = model.fit(x)
    labels = cluster_ms.fit_predict(x)
    nb_clusters = len(np.unique(labels))

    print("Mean Shift clustering done, number of clusters :", nb_clusters)

    save_model(f"{temp_dir}/mean_shift_model.pickle", cluster_ms)
    plot_cluster(x, labels + 1, nb_clusters, "mean_shift", temp_dir)

    return


def predict_labels(test: np.array, model_name: str, temp_dir: str):
    """
    Load a model and predict the labels for a testing set
    """
    predict_model = load_model(f"{temp_dir}/{model_name}_model.pickle")
    labels = predict_model.fit_predict(test)

    return labels


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "method",
        type=str,
        choices=["k", "h", "d"],
        help="Specify the method of clustering, k=kmean, h=hierarchical, d=dbscan",
    )
    parser.add_argument(
        "-n",
        type=int,
        choices=range(2, 8),
        default=7,
        help="If kmeans is chosen, specify the number of clusters, default is 7",
    )
    args = parser.parse_args()
    method = args.method
    nb_clusters = args.n

    if method == "k":
        kmeans_cluster(nb_clusters)

    elif method == "h":
        hierarchical_cluster()

    elif method == "d":
        dbscan_cluster(np.array([0, 1], [1, 0]))

    else:
        print("wrong method")
