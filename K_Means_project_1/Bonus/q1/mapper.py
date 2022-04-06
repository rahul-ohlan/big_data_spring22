#!/usr/bin/python

import sys



for line in sys.stdin:

    line = line.strip()
    line = line.split(',')
    if line[0] == "Summons Number":
        continue
    

    if line[33] in ["Black", "BLK", "BK", "BK.", "BLAC", "BK/","BCK","BLK.","B LAC","BC"]:
        color = "black"
    
    else:
        color = "not_black"

    if line[9] in ["34510", "10030", "34050"] or line[10] in ["34510", "10030", "34050"] or line[11] in ["34510", "10030", "34050"]:

        print(color+"\t"+"1")