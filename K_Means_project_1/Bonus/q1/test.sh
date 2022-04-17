#!/bin/bash


start-all.sh

hdfs dfsadmin -safemode leave

hadoop fs -rm -r /task1

hadoop fs -mkdir /task1


hadoop fs -put ./Parking_Violations_Issued_-_Fiscal_Year_2022.csv /task1

hadoop jar /usr/local/hadoop/share/hadoop/tools/lib/hadoop-streaming-3.3.1.jar \
	-file ./mapper.py -mapper ./mapper.py \
	-file ./reducer.py -reducer ./reducer.py \
	-input /task1/Parking_Violations_Issued_-_Fiscal_Year_2022.csv \
	-output /task1/output


hadoop fs -cat /task1/output/part-00000


hadoop fs -rm -r /task1


stop-all.sh
