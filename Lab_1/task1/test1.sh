#!/usr/bin/bash


# start clusters
start-all.sh

# clear hdfs directory
hadoop fs -rm -r /task1

# copy input data to hdfs directory

hadoop fs -mkdir /task1
hadoop fs -put ./access.log /task1

hadoop jar /usr/local/hadoop/share/hadoop/tools/lib/hadoop-streaming-3.3.1.jar \
        -file ./mapper1.py -mapper ./mapper1.py \
        -file ./reducer1.py -reducer ./reducer1.py \
        -input /task1/access.log \
        -output /task1/output

# access the output

hadoop fs -cat /task1/output/part-00000

# clean file system
hadoop fs -rm -r /task1

# shut down clusters
stop-all.sh