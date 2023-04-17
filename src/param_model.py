

class ParamModel:
    DBSCAN = dict(eps=8, min_samples=12, algorithm="auto")
    MeanShift = dict(bandwidth=None, cluster_all=False)
    KMeans = dict(n_clusters=7, n_init="auto", algorithm="lloyd")
    Hierarchical = dict(n_clusters=None, linkage="ward", distance_threshold=2000)
    Outlier = dict(n_estimators=100)
    SOM = dict(m=5, n=2, dim=2)