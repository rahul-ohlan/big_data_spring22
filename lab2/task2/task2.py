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
        print("Usage: wordcount <file>", file=sys.stderr)
        sys.exit(-1)

    spark = SparkSession\
        .builder\
        .appName("BonusQ1")\
        .getOrCreate()


    # access csv file in spark dataframe
    spark_df = spark.read.csv(sys.argv[1], header = True)

    # preprocess the file

    spark_df = spark_df.select(col('Street Code1'),col('Street Code2'),col('Street Code3'),col('Vehicle Color'))
    spark_df = spark_df.na.drop('any')
    spark_df = spark_df.withColumn('Street Code2',col('Street Code2').cast('int')).withColumn('Street Code3',col('Street Code3').cast('int'))
    
    
    # filter data on given street codes in order to find out conditional probability

    street_codes = [34510, 10030, 34050]
    codes = spark.sparkContext.broadcast(street_codes)
    spark_df = spark_df.filter(col('Street Code1').isin(codes.value)| col('Street Code2').isin(codes.value)| col('Street Code3').isin(codes.value))

    # broadcast black variable so it is accessible on the cluster
    black = ["BLACK","Black","BLK","BK","BK.","BLAC","BCK","BLK.","B LAC","BC"]
    broadcast_black = spark.sparkContext.broadcast(black)

    # now only the vehicle color column of spark_df is of essence

    car_color = spark_df.rdd.map(lambda loop : (loop['Vehicle Color'],1))
    car_color.cache()

    # filter cars on color : black | non_black

    def filter_black(car):

        if car[0] in broadcast_black.value:
            return ("black",1)
        else:
            return ("non_black",1)

    car_color1 = car_color.map(lambda tup : filter_black(tup))

    counts = car_color1.reduceByKey(add)

    # now we have counts of both kinds of cars
    # simply print the ratio (black / (black+non_black)) to get the probability

    def get_probability(count):

        num = count[0][1]
        den = num + count[1][1]

        return num/den

    counts =  counts.collect()

    proby = get_probability(counts)

    print("Probability that a 'BLACK' car will be tickedted on given Street Codes:",proby)

    spark.stop()
