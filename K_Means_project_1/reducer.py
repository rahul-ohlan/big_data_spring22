#! /c/Users/rahul.ohlan/AppData/Local/Microsoft/WindowsApps/python

from operator import itemgetter
import sys

import re
import errno

year_dict = dict()
type_dict = dict()

for line in sys.stdin:

    line = line.strip()
    line = line.split()
    year = line[0].split('_')[0]
    b_type = line[0].split('_')[1]
    num = line[1]
    num = int(num)

    year_dict[year] = year_dict.get(year,0) + num
    type_dict[b_type] = type_dict.get(b_type,0) + num


sorted_years = sorted(year_dict.items(), key = itemgetter(1),reverse=True)
sorted_types = sorted(type_dict.items(), key = itemgetter(1),reverse=True)

print('top 5 years: ',end=' ')
print(sorted_years[0:5])
print('top 5 car types: ',end=' ')
print(sorted_types[0:5])