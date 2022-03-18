# import csv

# with open('Parking_Violations_Issued_-_Fiscal_Year_2022.csv') as dataFile:
#     variable = csv.DictReader(dataFile)


#!usr/bin/python

import sys
import numpy as np
from numpy.linalg import norm


centroids = np.array(sys.argv[1] )       # any 4 random data points


cluster_map = dict()

for line in sys.stdin:

    line = line.strip()
    line = line.split()
    if "" in line:    # skip records with a missing value
        continue
    record = np.array(line)
    
    distance = np.zeros(len(centroids))
    for k in range(len(centroids)):

        row  = norm(record - centroids[k], axis = 1)
        distance[:,k] = np.square(row)
    
    nearest_cluster = np.argmin(distance,axis=1)

    if nearest_cluster in cluster_map:
        cluster_map[nearest_cluster].append([record,1])

    else:
        cluster_map[nearest_cluster] = list()
        cluster_map[nearest_cluster].append([record,1])

# combiner

for key, val in cluster_map.items():
    temp = np.zeros(len(val[0][0]))
    count = 0

    for v in val:
        temp += v[0]
        count += v[1]
    cluster_map[key] = [temp,count]

for key, val in cluster_map.items():
    print(str(key)+"\t",val)

    # val is a list which contains two things for each centroid(key) : 1. partial sum of all datapoints
                                                                    #  2. count of all datapoints
    # all this output will be sorted before getting to reducer, so can be taken advantage of 
    # take sum of all points from all mappers belonging to one centroid and divide by total count, ---> this will give new centroid of that cluster
    







