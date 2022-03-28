#!/usr/bin/python

from operator import itemgetter
import sys
import re
import errno


for line in sys.stdin:
    line = line.strip()
    line = line.split(',')

    year = str(line[35])

    if not (year!= '' and year!="Vehicle Year" and (int(year) > 1900 and int(year) < 2023)):
        continue           # skipping rows with invalid registration year data or missing values

    bodyType = str(line[6])

    if bodyType == "" or " " in bodyType or bodyType == "Vehicle Body Type":
        continue          # skipping rows with missing values of those containing spaces



    print(year+"_"+bodyType+"\t"+"1")