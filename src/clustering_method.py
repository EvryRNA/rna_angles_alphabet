import argparse
import os
from typing import Any

import numpy as np
from sklearn.cluster import DBSCAN, AgglomerativeClustering, KMeans

from src.scatter_plot import plot_cluster
from src.utils import save_model, load_model


def kmeans_cluster(X : np.array, nb_clusters : int):

    model = KMeans(n_clusters=nb_clusters, n_init="auto")
    cluster_kmeans = model.fit(X)
    labels = cluster_kmeans.fit_predict(X)

    print("Kmean clustering done, number of clusters :", nb_clusters)

    save_model("src/kmeans_model.pickle", cluster_kmeans)
    # plot_cluster(X, labels, nb_clusters, "k")

    return


def hierarchical_cluster(X : np.array):

    model = AgglomerativeClustering(n_clusters=None, linkage="ward", distance_threshold=2000)
    cluster_h = model.fit(X)
    labels = cluster_h.fit_predict(X)

    print("Hierarchical clustering done, number of clusters :", cluster_h.n_clusters_)

    save_model("src/hierarchical_model.pickle", cluster_h)
    # plot_cluster(X, labels, cluster_h.n_clusters_, "h")

    return


def dbscan_cluster(X : np.array):

    model = DBSCAN(eps=8, min_samples=12)
    cluster_db = model.fit(X)
    labels = cluster_db.fit_predict(X)
    nb_clusters = len(np.unique(labels))

    print("DBSCAN clustering done, number of clusters :", nb_clusters)

    save_model("src/dbscan_model.pickle", cluster_db)
    # plot_cluster(X, labels + 1, nb_clusters, "d")

    return


def predict_labels(test : np.array, model_name : str):

    predict_model = load_model(f"src/{model_name}_model.pickle")
    labels = predict_model.fit_predict(test)
    # os.remove(f"src/{model_name}_model.pickle")

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
        choices=range(2, 7),
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
        dbscan_cluster(np.array([0,1],[1,0]))

    else:
        print("wrong method")
