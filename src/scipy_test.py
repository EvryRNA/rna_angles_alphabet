import numpy as np
from scipy import stats
import matplotlib.pyplot as plt

from process_density import preprocess


x, y = preprocess()


values = np.array([x, y])

positions = np.vstack([x.ravel(), y.ravel()])

values = stats.gaussian_kde(values, bw_method="scott")

z = values(positions)

mean = np.mean(z)
std = np.std(z)
index = []

for j in range(0, len(z)):
    if z[j] < (mean + std):
        index.append(j)

x = np.delete(x, index)
y = np.delete(y, index)
z = np.delete(z, index)

# breakpoint()

fig, ax = plt.subplots(figsize=(9, 9), subplot_kw={"projection": "3d"})
surf = ax.plot_trisurf(x, y, z, cmap=plt.cm.jet)

plt.title("3D density plot", fontsize=20, loc="left")
fig.colorbar(surf, ax=ax, cmap=plt.cm.jet, aspect=3)
ax.view_init(45, -115)

plt.show()

