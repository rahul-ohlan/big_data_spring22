import sys

dict_ip_count = {}
dict_time_count = {}

for line in sys.stdin:

  time = line[0]
  ip = line[1][0]
  num = int(line[1][1])

  try:
    dict_ip_count[ip] = dict_ip_count.get(ip,0) + num
        
  except ValueError:
      pass


dict_ip_countlist = list(dict_ip_count.items())


dict_ip_countlist.sort(key=lambda x: x[1], reverse=True)


dict_ip_countlist = dict_ip_countlist[0:3]


for k in dict_ip_countlist:
  print(k[0],k[1])