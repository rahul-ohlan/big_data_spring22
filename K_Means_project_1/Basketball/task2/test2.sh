#!/bin/bash

centroids=("2.5 5 1" "11 4.5 5" "11 6 11" "25 6.5 14")

start-all.sh

hdfs dfsadmin -safemode leave

hadoop fs -rm -r /task2
hadoop fs -mkdir /task2
hadoop fs -put ./shot_logs.csv /task2




hdfs dfsadmin -safemode leave
echo "iteration number : $iter "
echo " input centroids : ${centroids[*]} "



hadoop jar /usr/local/hadoop/share/hadoop/tools/lib/hadoop-streaming-3.3.1.jar \
	-file ./bb_mapper.py -mapper ./"bb_mapper.py ${centroids[0]} ${centroids[1]} ${centroids[2]} ${centroids[3]}" \
	-file ./bb_reducer.py -reducer ./bb_reducer.py \
	-input /task2/shot_logs.csv \
	-output /task2/ouptut2


hadoop fs -cat /task2/output2/part-00000


stop-all.sh
