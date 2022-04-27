#!/bin/bash
source ../../../env.sh
/usr/local/hadoop/bin/hdfs dfs -rm -r /task1/input/
/usr/local/hadoop/bin/hdfs dfs -rm -r /task1/output
/usr/local/hadoop/bin/hdfs dfs -mkdir -p /task1/input/
hadoop dfs -put ./shot_logs.csv /task1/input/

/usr/local/spark/bin/spark-submit --master=spark://$SPARK_MASTER:7077 ./task1.py hdfs://$SPARK_MASTER:9000/task1/input/
