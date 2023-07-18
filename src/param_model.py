from sklearn.cluster import KMeans, MeanShift
from sklearn.ensemble import IsolationForest
from sklearn_som.som import SOM


class ParamModel:
    MeanShift = dict(
        bandwidth=None,  # default = None
        seeds=None,
        bin_seeding=False,
        min_bin_freq=1,
        cluster_all=False,  # default = False
        n_jobs=None,
        max_iter=300,
    )

    KMeans = dict(
        n_clusters=8,  # default = 16
        init="k-means++",
        n_init="auto",
        max_iter=300,
        tol=0.0001,
        verbose=0,
        random_state=None,
        copy_x=True,
        algorithm="lloyd",
    )

    # IsolationForest():
    Outlier = dict(
        n_estimators=100,
        max_samples="auto",
        contamination="auto",
        max_features=1.0,
        bootstrap=False,
        n_jobs=None,
        random_state=None,
        verbose=0,
        warm_start=False,
    )

    SOM = dict(m=4, n=4, dim=2, lr=1, max_iter=300)
    # Other options: sigma, max_iter, random_state


# Dictionary used to find the right function and parameters for each method
CONVERSION_NAME_TO_MODEL = {
    "mean_shift": {"class": MeanShift, "params": ParamModel.MeanShift},
    "kmeans": {"class": KMeans, "params": ParamModel.KMeans},
    "outlier": {"class": IsolationForest, "params": ParamModel.Outlier},
    "som": {"class": SOM, "params": ParamModel.SOM},
}
