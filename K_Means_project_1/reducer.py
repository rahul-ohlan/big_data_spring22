#! /c/Users/rahul.ohlan/AppData/Local/Microsoft/WindowsApps/python

from operator import itemgetter
import sys

import re
import errno

year_dict = dict()
type_dict = dict()

for line in sys.stdin:

    line = line.strip()
    year = line.split('_')[0]
    b_type = line.split('_')[1].split('\t')[0]
    num = line.split('_')[1].split('\t')[1]
    num = int(num)

    year_dict[year] = year_dict.get(year,0) + num
    type_dict[b_type] = type_dict.get(b_type,0) + num


sorted_years = sorted(year_dict, key = itemgetter(1),reverse=True)
sorted_types = sorted(type_dict, key = itemgetter(1),reverse=True)

print('top 5 years: ',end=' ')
print(sorted_years[0:5])
print('top 5 car types: ',end=' ')
print(sorted_types[0:5])





    # print(year,b_type)

    # print(line,end='')

