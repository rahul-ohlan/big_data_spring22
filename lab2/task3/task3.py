# -*- coding: utf-8 -*-
#
# Licensed to the Apache Software Foundation (ASF) under one or more
# contributor license agreements.  See the NOTICE file distributed with
# this work for additional information regarding copyright ownership.
# The ASF licenses this file to You under the Apache License, Version 2.0
# (the "License"); you may not use this file except in compliance with
# the License.  You may obtain a copy of the License at
#
#    http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
#

from __future__ import print_function

import sys
from operator import add

from pyspark.sql import SparkSession
from  pyspark.sql.functions import col
# reload(sys) 
# sys.setdefaultencoding('utf8')
if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: most_frequent_time <file>", file=sys.stderr)
        sys.exit(-1)

    spark = SparkSession\
        .builder\
        .appName("task3")\
        .getOrCreate()


    # access csv file in spark dataframe
    spark_df = spark.read.csv(sys.argv[1], header = True)

    # preprocess the file

    spark_df = spark_df.select(col('Issue Date'),col('Violation Time'))
    spark_df = spark_df.na.drop('any')    
    
    # change from dataframe to rdd for transformation

    spark_df = spark_df.rdd.map(lambda loop : (loop['Issue Date'],loop['Violation Time']))

    # next transformation: concatenate date and time to find most frequent combination
    def month_and_time(tup):
        date = tup[0]
        hours = tup[1]

        month = date[0:2]
        time = hours[0:2] + hours[-1]

        res = month + "-" + time

        return (res,1)


    spark_df2 = spark_df.map(lambda tup : month_and_time(tup))


    # get the most frequent value of month and time

    spark_df3 = spark_df2.reduceByKey(add)

    # now get the most frequent value
    spark_df4_sorted = spark_df3.sortBy(lambda tup : tup[1], ascending= False)

    # get and print the result lmao

    res = spark_df4_sorted.take(1)

    # process to get month and time
    values = res[0][0].split('-')
    month = values[0]
    time = values[1]

    print("********************")
    print()
    print()
    print("Vehicles are apparently most likely to be ticketed in",month+"th month","at",time)
    print()
    print()
    print("********************")


    spark.stop()
