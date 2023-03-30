import numpy as np
from sklearn.cluster import DBSCAN, AgglomerativeClustering, KMeans, MeanShift

from src.plot_helper import plot_cluster
from src.utils import load_model, save_model


def kmeans_cluster(x, nb_clusters: int, temp_dir: str):
    """
    Train a kmeans model on a dataset
    """
    model = KMeans(n_clusters=nb_clusters, n_init="auto")
    cluster_kmeans = model.fit(x)
    labels = cluster_kmeans.fit_predict(x)

    print("\nKmean clustering done, number of clusters :", nb_clusters, "\n")

    save_model(f"{temp_dir}/kmeans_model.pickle", cluster_kmeans)
    plot_cluster(x, labels, nb_clusters, "kmeans", temp_dir)

    return


def hierarchical_cluster(x, temp_dir: str):
    """
    Train a hierarchical model on a dataset
    """
    model = AgglomerativeClustering(n_clusters=None, linkage="ward", distance_threshold=2000)
    cluster_h = model.fit(x)
    labels = cluster_h.fit_predict(x)

    print("\nHierarchical clustering done, number of clusters :", cluster_h.n_clusters_, "\n")

    save_model(f"{temp_dir}/hierarchical_model.pickle", cluster_h)
    plot_cluster(x, labels, cluster_h.n_clusters_, "hierarchical", temp_dir)

    return


def dbscan_cluster(x, temp_dir: str):
    """
    Train a dbscan model on a dataset
    """
    model = DBSCAN(eps=8, min_samples=12)
    cluster_db = model.fit(x)
    labels = cluster_db.fit_predict(x)
    nb_clusters = len(np.unique(labels))

    print("\nDBSCAN clustering done, number of clusters :", nb_clusters, "\n")

    save_model(f"{temp_dir}/dbscan_model.pickle", cluster_db)
    plot_cluster(x, labels + 1, nb_clusters, "dbscan", temp_dir)

    return


def mean_shift_cluster(x, temp_dir: str):
    """
    Train a mean shift model on a dataset
    """
    model = MeanShift(bandwidth=None)
    cluster_ms = model.fit(x)
    labels = cluster_ms.fit_predict(x)
    nb_clusters = len(np.unique(labels))

    print("\nMean Shift clustering done, number of clusters :", nb_clusters, "\n")

    save_model(f"{temp_dir}/mean_shift_model.pickle", cluster_ms)
    plot_cluster(x, labels + 1, nb_clusters, "mean_shift", temp_dir)

    return


def predict_labels(test, model_name: str, temp_dir: str):
    """
    Load a model and predict the labels for a testing set
    """
    predict_model = load_model(f"{temp_dir}/{model_name}_model.pickle")
    labels = predict_model.fit_predict(test)
    print(type(labels))

    return labels
