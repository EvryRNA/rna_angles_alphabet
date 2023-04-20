class ParamModel:
    DBSCAN = dict(
        eps=8,
        min_samples=12,
        metric="euclidean",
        metric_params=None,
        algorithm="auto",
        leaf_size=30,
        p=None,
        n_jobs=None,
    )

    MeanShift = dict(
        bandwidth=None,
        seeds=None,
        bin_seeding=False,
        min_bin_freq=1,
        cluster_all=False,
        n_jobs=None,
        max_iter=300,
    )

    KMeans = dict(
        n_clusters=7,
        init="k-means++",
        n_init="auto",
        max_iter=300,
        tol=0.0001,
        verbose=0,
        random_state=None,
        copy_x=True,
        algorithm="lloyd",
    )

    # AgglomerativeClustering():
    Hierarchical = dict(
        n_clusters=None,
        affinity="deprecated",
        metric=None,
        memory=None,
        connectivity=None,
        compute_full_tree="auto",
        linkage="ward",
        distance_threshold=2000,
        compute_distances=False,
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

    SOM = dict(m=5, n=2, dim=2, lr=1)  # Options: sigma, max_iter, random_state
