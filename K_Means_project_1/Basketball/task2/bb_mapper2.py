#!/usr/bin/python

import sys
import numpy as np
from numpy.linalg import norm

final_centroids = list(sys.argv[1], sys.argv[2], sys.argv[3], sys.argv[4])

results = dict()

for line in sys.stdin:

    line = line.strip()
    line = line.split(',')

    if line[0] == "GAME_ID":
        continue

    if line[9] == "":
        continue
    shot_dist = float(line[12])
    close_def_dist = float(line[18])
    shot_clock = float(line[9])
    player_name = line[21].lower()
    shot_status = line[14]

    if not line[15].startswith('"'):
        player_name = line[20].lower()
        close_def_dist = float(line[17])

    datapoint = np.array([shot_dist,close_def_dist,shot_clock])


    if player_name in ['james harden', 'chris paul', 'stephen curry', 'lebron james']:

        # find which zone this particular datapoint of this player lies in
        k = len(final_centroids)      # k = 4
        distance = np.zeros(k)
        for i in range(k):

            row = norm(datapoint-final_centroids[i], axis = 0)
            distance[i] = np.square(row)

        nearest_centroid = np.argmin(distance,axis = 0)

        # now for this player_name, this datapoint lies in the cluster nearest_centroid
        # now we need to keep track of shots missed and made in this record

        if player_name not in results:
            results[player_name] = dict()

        if nearest_centroid not in results[player_name]:
            results[player_name][nearest_centroid] = list()
        
        # now just append made and missed scores
        if shot_status == 'made':
            results[player_name][nearest_centroid].append(np.array([1,0]))

        else:
            results[player_name][nearest_centroid].append(np.array([0,1]))


    else:
        continue


# now we have a results dictionary with each player having the short status in each zone

# combiner
# transform the short status to total shots made and total shots missed
for key, val in results.items():

    # val is a dictionary of zones
    for zone in val:

        val[zone] = np.array(val[zone])
        val[zone] = np.sum(val[zone],axis=0)

# now we have results dictionary containing total made and missed shots in each zone for each of the four players

for key, val in results.items():

    player = key
    for k,v in val.items():
        zone = k
        shots_made = v[0]
        shots_missed = v[1]

        print(player + "\t" + str(zone)+"_"+str(shots_made)+"_"+str(shots_missed))