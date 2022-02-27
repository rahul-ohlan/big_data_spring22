#!/usr/bin/python
# --*-- coding:utf-8 --*--

import sys

dict_ip_count = {}
dict_time_count = {}

for line in sys.stdin:
    time = line[0]
    ip = line[1][0]
    num = line[1][1]
    try:
        num = int(num)
        if time in dict_time_count:
          if ip in dict_time_count[time]:

            dict_time_count[time][ip] += num
          else:
            dict_time_count[time][ip] = 1
          
        else:
          new = {}
          new[ip] =  1
          dict_time_count[time] = new
         
    except ValueError:
        pass



for key, value in dict_time_count.items():
  count_list = list(value.items())
  count_list.sort(key=lambda x: x[1], reverse=True)
  dict_time_count[key]=count_list[0:3]  
for key, values in dict_time_count.items():
  print(key)
  for i in values:
    print(i)