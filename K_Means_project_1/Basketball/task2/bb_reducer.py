#!/usr/bin/python


import sys
import numpy as np
from operator import itemgetter

updated_centroids = dict()


for line in sys.stdin:           # 2        45435_65467_464757657_7658576

    line = line.strip()
    line = line.split('\t')
    centroid = line[0]

    datapoints = line[1].split('_')
    points = [float(x) for x in datapoints[0:3]]
    count = float(datapoints[3])
    datapoints = list()
    datapoints.append(points)
    datapoints.append(count)            # [[45435, 65467, 464757657], 7658576] = datapoints
    
        #datapoints is a list of partial sum and partial count from each mapper

    if centroid in updated_centroids:
        updated_centroids[centroid].append(datapoints)

    else:
        updated_centroids[centroid] = list()
        updated_centroids[centroid].append(datapoints)     #  { '0' :  # [  [[45435, 65467, 464757657], 7658576], . . .] , '1' :  . . . }


# updated centroids has now keys as labels of centroids, but not the actual datapoint of centroids
# values against each centroid has a list of list. with inner lists as partial sums and counts from each mapper belonging to that centroid label
# now we need to get updated centroids for each cluster by taking mean of datapoints for each cluster
for key, val in updated_centroids.items():

    temp = np.zeros(len(val[0][0]))     # [0,0,0]
    count = 0

    for v in val:
        temp += np.array(v[0])
        count += v[1]
    mean_centroids = np.around(temp/count,decimals=3)   # total sum of all points divided by total number of points equals mean of all the datapoints in the cluster
    updated_centroids[key] = " ".join([str(x) for x in mean_centroids])

# temp is an array of three points for each cluster
# need to convert it to a string
fc = sorted(updated_centroids.items(), key = itemgetter(0)) 
for item in fc:

    print(str(item[1]))
