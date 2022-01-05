import numpy as np
from scipy.spatial import Voronoi, voronoi_plot_2d
import matplotlib
matplotlib.use('agg')
import matplotlib.pyplot as plt

points = []
for line in open("station_points.csv"):
    p = line.strip().split(",")
    points.append([float(p[1]), float(p[0])])
pnp = np.array(points)
vor = Voronoi(pnp)
fig = voronoi_plot_2d(vor)
fig.set_size_inches(40, 40)
fig.savefig('myfig.png')

x = [-71.2, -71]
y = [42.25, 42.43]
