#!/usr/bin/python

import sys
import numpy as np
from numpy.linalg import norm
from operator import itemgetter

res = dict()

for line in sys.stdin:

    # line is like james harden    0_1     (zone and count)
    # need to add all counts for every zone and pick the one with minimum count

    line = line.strip()
    line = line.split("\t")

    zone = line[0]
    count = float(line[1])


    res[zone] = res.get(zone,0) + count
    


# now we have number of parking tickets for each zone from every mapper
# just print the zone with minimum number of parking tickets as the preferable zone to park


    # key = zone ( 0 or 1 or 2 or 3 or whatever)
    # val  = count of parking tickets

sorted_zones = sorted(res.items(),key = itemgetter(1))

print('Most Favorable Zone to Park Near Lincoln Center:',sorted_zones[0][0])
