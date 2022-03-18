#!usr/bin/python

import sys
from turtle import update

updated_centroids = dict()
prev_centroids = dict()

for line in sys.stdin:

    line = line.strip()
    line = line.split('\t')
    centroid = line[0]
    datapoints = line[1]    #datapoints is a list of partial sum and partial count from each mapper

    if centroid in updated_centroids:
        updated_centroids[centroid].append(datapoints)

    else:
        updated_centroids[centroid] = list()
        updated_centroids[centroid].append(datapoints)

# updated centroids has now keys as labels of centroids, but not the actual datapoint of centroids
# values against each centroid has a list of list. with inner lists as partial sums and counts from each mapper belonging to that centroid label
# now we need to get updated centroids for each cluster by taking mean of datapoints for each cluster
for key, val in updated_centroids.items():

    temp = np.zeros(len(val[0][0]))
    count = 0

    for v in val:
        temp += v[0]
        count += v[1]
    updated_centroids[key] = temp/count   # total sum of all points divided by total number of points equals mean of all the datapoints in the cluster

final_centroids = list()
for key, val in updated_centroids.items():
    final_centroids.append(val)

print(final_centroids)


    

