#!usr/bin/python

import sys
import numpy as np
from numpy.linalg import norm


centroids = np.array(sys.argv[1], sys.argv[2], sys.argv[3],sys.argv[4] )       # any 4 random data points


cluster_map = dict()

for line in sys.stdin:

    line = line.strip()
    line = line.split(',')

    shot_dist = line[12]
    close_def_dist = line[18]
    shot_clock = line[9]
    player_name = line[21].lower()
    
    if line[0] == 'GAME_ID'  or shot_clock =='':   # skip first row, and, shot_clock is the only column with missing values
        continue

    datapoint = np.array([shot_dist,close_def_dist,shot_clock])

    distance = np.zeros(len(centroids))
    for k in range(len(centroids)):

        row  = norm(datapoint - centroids[k], axis = 0)    
        distance[k] = np.square(row)
    
    nearest_cluster = np.argmin(distance,axis=0)

    if nearest_cluster in cluster_map:
        cluster_map[nearest_cluster].append([datapoint,1])

    else:
        cluster_map[nearest_cluster] = list()
        cluster_map[nearest_cluster].append([datapoint,1])

# combiner


for key, val in cluster_map.items():
    temp = np.zeros(len(val[0][0]))  
    count = 0

    for v in val:
        temp += v[0] 
        count += v[1]
    cluster_map[key] = [temp,count]



for key, val in cluster_map.items():
    zone = str(key)
    f = val[0][0]
    s = val[0][1]
    t = val[0][2]
    c = val[1]
    print(zone+"\t"+str(f)+"_"+str(s)+"_"+str(t)+_str(c))

    # val is a list which contains two things for each centroid(key) : 1. partial sum of all datapoints
                                                                    #  2. count of all datapoints
    # all this output will be sorted before getting to reducer, so can be taken advantage of 
    # take sum of all points from all mappers belonging to one centroid and divide by total count, ---> this will give new centroid of that cluster
    







