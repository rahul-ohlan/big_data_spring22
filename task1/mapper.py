#!/usr/bin/python
# --*-- coding:utf-8 --*--
import re
import sys

pat = re.compile('(?P<ip>\d+.\d+.\d+.\d+).*?\d{4}:(?P<hour>\d{2}):\d{2}.*? ')
for line in sys.stdin:
    match = pat.search(line)
    if match:
        data = ('%s\t%s' % ('[' + match.group('hour') + ':00' + ']' + match.group('ip'), 1))
        data = data.strip()
        time = data[1:6]
        ip = data[7:]
        ip,num = ip.split('\t')
        if (':' not in ip) and (ip.count('.')==3):
        print(time,(ip,num))