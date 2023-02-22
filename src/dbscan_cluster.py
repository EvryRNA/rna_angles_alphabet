from sklearn.cluster import DBSCAN
import numpy as np
import matplotlib.pyplot as plt

from process_density import preprocess


x, y = preprocess()
angles = np.empty((11433, 2))

for i in range(0, len(x)):
    angles[i,0] = x[i]
    angles[i,1] = y[i] 


print(angles)

