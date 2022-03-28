#!/usr/bin/python

import sys
import numpy as np

mapper_dict = dict()
for line in sys.stdin:

    line = line.strip()
    line = line.split(',')

    if line[0] == 'GAME_ID': # skip header row
        continue

    shot_clock = line[9]
    player_name = line[21].lower()
    if line[15].startswith('"'):
        def_last_name = line[15][1:]
        def_first_name = line[16][:-1]
        def_name = def_first_name + " " + def_last_name
    
    else:
        def_name = line[15]
        player_name = line[20].lower()
    
    shot_status = line[14]   # made / missed
    
    if  shot_clock =='':   # skip missing values
        continue

    if player_name not in mapper_dict:
        mapper_dict[player_name] = dict()

    if def_name not in mapper_dict[player_name]:
        mapper_dict[player_name][def_name] = list()

    if shot_status == 'made':
        mapper_dict[player_name][def_name].append(np.array([1,0]))
    else:
        mapper_dict[player_name][def_name].append(np.array([0,1]))

    


for key, val in mapper_dict.items():

    for k,v in val.items():
        
        v = np.array(v)
        v = np.sum(v,axis = 0)  
        val[k] = v


# now or dictionary is ready for output to reducer

for key, val in mapper_dict.items():

    for k,v in val.items():
        
        print(key + "\t" + k+"_"+str(v[0])+"_"+str(v[1]))




