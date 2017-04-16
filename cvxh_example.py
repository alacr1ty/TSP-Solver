import numpy as np
from scipy.spatial import ConvexHull
import matplotlib.pyplot as plt


# Generate some random points for the demo.
np.random.seed(4321)
pts = 0.1 + 0.8*np.random.rand(15, 2)

print 'hey!'

ch = ConvexHull(pts)

# print ch

# Get the indices of the hull points.
hull_indices = ch.vertices

print 'ho! lets go!'

# These are the actual points.
hull_pts = pts[hull_indices, :]

plt.plot(pts[:, 0], pts[:, 1], 'ko', markersize=10)
plt.fill(hull_pts[:,0], hull_pts[:,1], fill=False, edgecolor='b')
plt.xlim(0, 1)
plt.ylim(0, 1)
plt.show()