#! ./bin/hy
#! ./bin/hy

import numpy as np
import scipy.linalg as la
import matplotlib.pyplot as plt

def monte_estimate(n):
    points = np.random.uniform(-1,1, size=(2,n))
    lengths = la.norm(points, axis=0)
    num_within = np.count_nonzero(lengths < 1)
    out = 4 * (num_within / n)
    inner_mask = lengths < 1
    outer_mask = lengths >= 1
    plt.scatter(points[0][inner_mask], points[1][inner_mask], color="orange")
    plt.scatter(points[0][outer_mask], points[1][outer_mask], color="blue")
    plt.title(f"{n} points; pi = {out}")
    plt.show()
    return out

for i in [500, 2000, 8000]:
    print(monte_estimate(i))
