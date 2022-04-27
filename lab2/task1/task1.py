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
import numpy as np

from pyspark.sql import SparkSession
from pyspark.sql.functions import col
from pyspark.ml.clustering import KMeans
from pyspark.ml.evaluation import ClusteringEvaluator
from pyspark.ml.feature import VectorAssembler

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: comfortable_zones <file>", file=sys.stderr)
        sys.exit(-1)

    spark = SparkSession\
        .builder\
        .appName("Comfortable_Zones")\
        .getOrCreate()

    # get sparkDataFrame
    spark_df = spark.read.csv(sys.argv[1],header=True)
    # drop null values
    spark_df = spark_df.na.drop('any')
    # select only the required features for training kmean
    # change to float types
    spark_df = spark_df.withColumn('SHOT_DIST',col('SHOT_DIST').cast('float')).withColumn('CLOSE_DEF_DIST',col('CLOSE_DEF_DIST').cast('float')).withColumn('SHOT_CLOCK',col('SHOT_CLOCK').cast('float'))

    # remove ouliers
    spark_df = spark_df.where((col('SHOT_DIST') < 31 ) & (col('CLOSE_DEF_DIST') < 15))

    spark_df.cache()
    spark_df1 = spark_df.select(col('SHOT_DIST'),col('CLOSE_DEF_DIST'),col('SHOT_CLOCK'))
    # transform dataframe to be used for kmeans

    required_features = ['SHOT_DIST', 'CLOSE_DEF_DIST', 'SHOT_CLOCK']
    assembler = VectorAssembler(inputCols=required_features, outputCol = 'features')

    transformed_data = assembler.transform(spark_df1)

    # import classifier
    kmeans = KMeans().setK(4).setSeed(33)

    # train data on the whole input dataset
    model = kmeans.fit(transformed_data)


    spark_df = spark_df.select(col('SHOT_DIST'),col('CLOSE_DEF_DIST'),col('SHOT_CLOCK'),col('player_name'),col('SHOT_RESULT'))

    # get datasets for the 4 players
    lebron_james = spark_df.where(col('player_name') == 'lebron james')
    james_harden = spark_df.where(col('player_name') == 'james harden')
    chris_paul = spark_df.where(col('player_name') == 'chris paul')
    stephen_curry = spark_df.where(col('player_name') == 'stephen curry')


    # get zones for each of the players records

    required_features = ['SHOT_DIST', 'CLOSE_DEF_DIST', 'SHOT_CLOCK']
    assembler = VectorAssembler(inputCols=required_features, outputCol = 'features')

    lebron_james_ = assembler.transform(spark_df)
    james_harden_ = assembler.transform(james_harden)
    chris_paul_ = assembler.transform(chris_paul)
    stephen_curry_ = assembler.transform(stephen_curry)


    predictions_lj = model.transform(lebron_james_)
    predictions_jh = model.transform(james_harden_)
    predictions_cp = model.transform(chris_paul_)
    predictions_sc = model.transform(stephen_curry_)


    # getting hit zone with maximum hit rate for lebron james
    predRDD_lj = predictions_lj.rdd.map(lambda loop : (loop['SHOT_RESULT'], loop['prediction']))
    predRDD_jh = predictions_jh.rdd.map(lambda loop : (loop['SHOT_RESULT'], loop['prediction']))
    predRDD_cp = predictions_cp.rdd.map(lambda loop : (loop['SHOT_RESULT'], loop['prediction']))
    predRDD_sc = predictions_sc.rdd.map(lambda loop : (loop['SHOT_RESULT'], loop['prediction']))

    predRDD_lj = predRDD_lj.groupBy(lambda tup : tup[1])
    predRDD_jh = predRDD_jh.groupBy(lambda tup : tup[1])
    predRDD_cp = predRDD_cp.groupBy(lambda tup : tup[1])
    predRDD_sc = predRDD_sc.groupBy(lambda tup : tup[1])

    def get_hit_rate(tup):

        zone = tup[0]
        status = tup[1]   # status = [('made',1),('missed',1),...]

        num, den = 0,0

        for ele in status:
            if ele[0] == 'made':
                num +=1

            else:
                den +=1


        return (zone,num/(num+den))


    predRDD_group = predRDD_lj.map(lambda tup : get_hit_rate(tup))

    # print the zone with maximum hit rate in the group

    res_lj = predRDD_group

    
    try:
        arr_lj = res_lj.collect()

        best_hit_rate1 = float('-inf')
        comfortable_zone1 = None
        for item in arr_lj:
            zone = item[0]
            hit_rate = item[1]
            if hit_rate > best_hit_rate1:
                best_hit_rate1 = hit_rate
                comfortable_zone1 = zone
    except:
        pass



    ###########################################
    predRDD_group = predRDD_jh.map(lambda tup : get_hit_rate(tup))

    # print the zone with maximum hit rate in the group

    res_jh = predRDD_group

    try:
        arr_jh = res_jh.collect()

        best_hit_rate2 = float('-inf')
        comfortable_zone2 = None
        for item in arr_jh:
            zone = item[0]
            hit_rate = item[1]
            if hit_rate > best_hit_rate2:
                best_hit_rate2 = hit_rate
                comfortable_zone2 = zone

    except:
        pass

    ###############################################

    predRDD_group = predRDD_sc.map(lambda tup : get_hit_rate(tup))

    res_sc = predRDD_group

    try:
        arr_sc = res_sc.collect()

        best_hit_rate3 = float('-inf')
        comfortable_zone3 = None
        for item in arr_sc:
            zone = item[0]
            hit_rate = item[1]
            if hit_rate > best_hit_rate3:
                best_hit_rate3 = hit_rate
                comfortable_zone3 = zone

    except:
        pass

    ####################################################

    predRDD_group = predRDD_cp.map(lambda tup : get_hit_rate(tup))


    res_cp = predRDD_group

    try:
    
        arr_cp = res_cp.collect()

        best_hit_rate4 = float('-inf')
        comfortable_zone4 = None
        for item in arr_cp:
            zone = item[0]
            hit_rate = item[1]
            if hit_rate > best_hit_rate4:
                best_hit_rate4 = hit_rate
                comfortable_zone4 = zone

    
    except:
        pass

    print('Most comfortable zone for Lebron James:',comfortable_zone1,'with a hit rate of:',best_hit_rate1)
    print('Most comfortable zone for James Harden:',comfortable_zone2,'with a hit rate of:',best_hit_rate2)
    print('Most comfortable zone for Stephen Curry:',comfortable_zone3,'with a hit rate of:',best_hit_rate3)
    print('Most comfortable zone for Chris Paul:',comfortable_zone4,'with a hit rate of:',best_hit_rate4)

    spark.stop()
