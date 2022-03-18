#!/usr/bin/bash


# take user input
echo "Please enter the time range (ex. 0-1 is 00:00 - 01:00 hrs):"
read use_input
echo "thanks!"

# start the cluster

start-all.sh
hadoop dfsadmin -safemode leave

# clean the file system

hadoop fs -rm -r /task2

# copy access.log to hdfs input directory

hadoop fs -mkdir /task2
hadoop fs -put ./access.log /task2/

# run task2 on hdfs

hadoop jar /usr/local/hadoop/share/hadoop/tools/lib/hadoop-streaming-3.3.1.jar \
        -file ./mapper2.py -mapper "./mapper2.py $use_input" \
        -file ./reducer2.py -reducer ./reducer2.py \
        -input /task2/access.log \
        -output /task2/output


# access output

hadoop fs -cat /task2/output/part-00000

# clean the file system
hadoop fs -rm -r /task2

# stop the cluster

stop-all.sh
