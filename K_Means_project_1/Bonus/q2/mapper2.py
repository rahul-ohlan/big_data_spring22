#!/usr/bin/python

import sys
import numpy as np
from numpy.linalg import norm
import re


c1 = np.array(sys.argv[1].split()).astype(np.float64)       # any 6 random data points
c2 = np.array(sys.argv[2].split()).astype(np.float64)   
c3 = np.array(sys.argv[3].split()).astype(np.float64)
c4 = np.array(sys.argv[4].split()).astype(np.float64)




pat_st_name = re.compile(r'^W\s[5-7][0-9]')    # to fetch W 57 from street name
pat_st_num = re.compile((r'\d\d'))             # to fetch 57 from street name

final_centroids = np.array([c1,c2,c3,c4])

for line in sys.stdin:

    line = line.strip()
    line = line.split(',')

    if line[0] == "Summons Number":         # skip the header row
        continue

    precinct = int(line[14])                # Manhattan North has precinct  = 20 (fetch the 0.5 mile radius)
    street_name = line[24]
    time = line[19]

    if len(time)!=5:                      # must be a 5-character string
        continue

    hours = int(time[0:4])                # example : 1030
    shift = time[4]                       # Am or Pm



    # Data Filters:
    # Streets taken from W 52 till W 72
    # Precinct = 20 restricts area close to Lincoln Center (0.5 Miles) on those streets
    # time window taken from 9.30 AM till 10.30 AM (assuming car will be parked around 10 AM)

    if shift!="A" or (hours < 930 or hours > 1030):
        continue

    if precinct!= 20:
        continue

    street_name = pat_st_name.findall(street_name)          # ['W 66']
    if street_name:
        street_name = street_name[0]                        # 'W 66'
        street_num = pat_st_num.findall(street_name)        # ['66']
        if not street_num:
            continue
        else:
            street_num = int(street_num[0])                 # 66

    else:
        continue

       

    # Restricting Area under consideration using street numbers
    if street_num > 72 or street_num < 52 :
        continue
    

    # finall we have the data we need!

    sc1 = float(line[9])
    sc2 = float(line[10])
    sc3 = float(line[11])

    if not sc1 or not sc2 or not sc3:
        continue

    datapoint = np.array([sc1,sc2,sc3])



    # find which zone this particular datapoint of this player lies in
    k = len(final_centroids)      # k = 4
    distance = np.zeros(k)

    for i in range(k):

        row = norm(datapoint-final_centroids[i], axis = 0)
        distance[i] = np.square(row)

    nearest_centroid = np.argmin(distance,axis = 0)

    # now we have the zone to which this datapoint is closest to 
    # need to collect the set of datapoints that are closest to this zone through mapper
    # and whether there was a violation ticket at this datapoint

    print(nearest_centroid+"\t"+"1")

