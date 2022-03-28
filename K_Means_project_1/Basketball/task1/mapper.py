#!usr/bin/python

import sys
import numpy as np

mapper_dict = dict()
for line in sys.stdin:

    line = line.strip()
    line = line.split(',')

    shot_clock = line[9]
    player_name = line[21].lower()
    def_first_name = line[16][:-1]
    def_last_name = line[15][1:]
    def_name = def_first_name + " " + def_last_name
    shot_status = line[14]   # made / missed
    
    if line[0] == 'GAME_ID'  or shot_clock =='':   # skip first row, and, shot_clock is the only column with missing values
        continue

    if player_name not in mapper_dict:
        mapper_dict[player_name] = dict()

    if def_name not in mapper_dict[player_name]:
        mapper_dict[player_name][def_name] = list()

    if shot_status == 'made':
        mapper_dict[player_name][def_name].append(np.array([1,0]))
    else:
        mapper_dict[player_name][def_name].append(np.array([0,1]))

    
# now we have a dictionary of this kind:

# {brian roberts : {alan anderson : [[1,0],[1,0],[0,1],[0,1],[0,1]]
#                   bojan bogdanaovic : [[1,0],[0,1]] }}
# for all the players and their defenders with their short statuses

# combiner - let's aggregate all the sots made and missed so as to calculate the hit rate
# in reducer

for key, val in mapper_dict.items():
    # key is player_name
    # val is dictionary of defenders with individual shot statuses
    for k,v in val:
        # k is defender's name
        # v is a list of np arrays of short status
        v = np.array(v)
        v = np.sum(v,axis = 0)  # get sum of all those short statuses in one single array


# now or dictionary is ready for output to reducer

for key, val in mapper_dict.items():

    for k,v in val:
        
        print(key + "\t" + k+"_"+str(v[0])+"_"+str(v[1])


# outputs like brian roberts         alan anderson_45_23
# in reducer make sure split is not based off the space character, but must be on the tab character



