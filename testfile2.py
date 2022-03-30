#!/usr/bin/python


import sys
import numpy as np
from numpy.linalg import norm
print(sys.argv[1], sys.argv[2], sys.argv[3], sys.argv[4])

c1 = np.array(sys.argv[1].split()).astype(np.float64)
c2 = np.array(sys.argv[2].split()).astype(np.float64)
c3 = np.array(sys.argv[3].split()).astype(np.float64)
c4 = np.array(sys.argv[4].split()).astype(np.float64)

centroids = np.array([c1,c2,c3,c4])

datapoint = np.array([7.7,1.3,10.8])
distance = np.zeros(len(centroids))

for k in range(len(centroids)):

    row = norm(datapoint - centroids[k], axis = 0)
    distance[k] = np.square(row)

nearest_cluster = np.argmin(distance,axis = 0)

print(distance)
print(nearest_cluster)
