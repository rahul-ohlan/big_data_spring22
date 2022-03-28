#! usr/bin/python


import sys
import numpy as np
from operator import itemgetter


res = dict()

for line in sys.stdin:

    line = line.strip()
    line = line.split('\t')

    player_name = line[0]

    gibberish = line[1].split('_')

    def_name = gibberish[0]
    made = gibberish[1]
    missed = gibberish[2]

    if player_name not in res:
        res[player_name] = dict()

    res[player_name][def_name] = res[player_name].get(def_name,np.array([0,0])) + np.array([made,missed])

# now we have aggregate of all the mappers
# calculate hit rate now

for key, val in res.items():

    # key is player name
    # val is a dictionary with defender names and their made miss counts

    for k,v in val.items():
        # k is defender name
        md = v[0]
        mis = v[1]
        hit_rate = md/(md+mis)
        val[k] = hit_rate

# now the dictionary contains hit rate for each defender for each shot taken by a player

for key , val in res.items():

    sorted_defenders = sorted(val.items(), key = itemgetter(1))
    res[key] = sorted_defenders


# now for each player, just print the defender with lowest hit rate

for key, val in res.items():

    print(res[key], "  Worst Defender: -->", val[0][0])


