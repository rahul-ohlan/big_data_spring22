#!/usr/bin/python

import sys
import numpy as np
from numpy.linalg import norm
from operator import itemgetter

res = dict()

for line in sys.stdin:

    # line is like james harden    0_54_26

    line = line.strip()
    line = line.split()
    player_name = line[0]
    scores = line[1]
    scores = scores.strip()
    scores = scores.split('_')

    nearest_centroid = scores[0]
    points_made = int(scores[1])
    points_missed = int(scores[2])


    # now need to res the points from each mapper
    if player_name not in res:
        res[player_name] = dict()

    if nearest_centroid not in res[player_name]:
        res[player_name][nearest_centroid] = np.array([0,0])

    res[player_name][nearest_centroid] += np.array([points_made,points_missed])


# now we finally have aggregate of all the points made and missed for each player in each zone
# now calculate and report the hit rate

for key, val in res.items():

    # key = stephen curry
    # val = { 0 : [made,missed], 1 : ...}
    for k,v in val.items():

        made = v[0]
        missed = v[1]
        hit_rate = made/(made+missed)
        val[k] = hit_rate


# now we have hit rate in each zone for each of the four players
# report the zones with maximum hit rates

for key, val in res.items():

    # key = lebron james
    # val = { 0 : 0.45, 1 : 0.67 ...}

    sorted_hit_rates = sorted(val.items(),key = itemgetter(1), reverse=True)
    
    print('Player:',key)
    print('Most Favorable Zone:',sorted_hit_rates[0][0])
    print('Hit Rate:',sorted_hit_rates[0][1])