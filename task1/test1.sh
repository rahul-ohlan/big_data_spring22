#!/bin/bash
../../start.sh
/usr/local/hadoop/bin/hdfs dfs -rm -r /task1/input/
/usr/local/hadoop/bin/hdfs dfs -rm -r /task1/output/
/usr/local/hadoop/bin/hdfs dfs -mkdir -p /task1/input/
/usr/local/hadoop/bin/hdfs dfs -copyFromLocal ../../mapreduce-test-data/access.log /task1/input/
/usr/local/hadoop/bin/hadoop jar /usr/local/hadoop/share/hadoop/tools/lib/hadoop-streaming-3.3.1.jar \
-file ../../mapreduce-test-python/task1/mapper.py -mapper ../../mapreduce-test-python/task1/mapper.py \
-file ../../mapreduce-test-python/logstat/reducer.py -reducer ../../mapreduce-test-python/task1/reducer.py \
-input /task1/input/* -output /task1/output/
/usr/local/hadoop/bin/hdfs dfs -cat /task1/output/part-00000
/usr/local/hadoop/bin/hdfs dfs -rm -r /task1/input/
/usr/local/hadoop/bin/hdfs dfs -rm -r /task1/output/
../../stop.sh