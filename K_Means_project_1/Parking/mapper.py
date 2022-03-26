#! /c/Users/rahul.ohlan/AppData/Local/Microsoft/WindowsApps/python

from operator import itemgetter
import sys
import re
import errno

f_handle = open('Parking_Violations_Issued_-_Fiscal_Year_2022.csv')

c = 0
data = f_handle.readlines()

for line in data:
    line = line.strip()
    line = line.split(',')

    year = str(line[35])

    if not (year!= '' and year!="Vehicle Year" and (int(year) > 1900 and int(year) < 2023)):
        continue           # skipping rows with invalid registration year data or missing values

    bodyType = str(line[6])

    if bodyType == "" or " " in bodyType or bodyType == "Vehicle Body Type":
        continue          # skipping rows with missing values of those containing spaces



    print(year+"_"+bodyType+"\t"+"1")


    if c==10:
        break

    c+=1

f_handle.close()