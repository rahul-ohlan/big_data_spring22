#! /c/Users/rahul.ohlan/AppData/Local/Microsoft/WindowsApps/python

from operator import itemgetter
import sys
import re
import errno

f_handle = open('Parking_Violations_Issued_-_Fiscal_Year_2022.csv')

c = 0
data = f_handle.readlines()
# data = iter(data)
# next(data)
# year_pat = re.compile(r'^\d\d\d\d$')
# body_type_pat = re.compile(r'^[a-zA-Z]+\S$')
for line in data:
    line = line.strip()
    line = line.split(',')

    year = str(line[35])

    if not (year!= '' and year!="Vehicle Year" and (int(year) > 1900 and int(year) < 2023)):
        continue           # skipping rows with invalid registration year data

    bodyType = str(line[6])

    if bodyType == "" or " " in bodyType or bodyType == "Vehicle Body Type":
        continue          # skipping rows with missing values of those containing spaces



    print(year+"_"+bodyType+"\t"+"1")


    if c==10:
        break

    c+=1
    # try:
    #     reg_year = year_pat.search(line[35])
    # except:
    #     reg_year = "None"

    # if reg_year:
    #     reg_year = reg_year[0]
    # body_type = body_type_pat.search(line[6])

    # if  body_type and line[6]!="Vehicle Body Type":
    #     body_type = body_type[0]
    # else:
    #     body_type = "None"

    # if c==3:
    #     break
    # print(reg_year+"\t"+body_type)


f_handle.close()