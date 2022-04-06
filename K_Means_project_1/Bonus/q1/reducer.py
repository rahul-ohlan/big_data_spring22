#!/usr/bin/python

import sys


res = dict()
for line in sys.stdin:

    line = line.split("\t")
    color = line[0]
    count = float(line[1])

    res[color] = res.get(color,0) + count


num = res['black']
den = res['black'] + res['not_black']

proby = num/(num+den)

print("required probability:",proby)