#!/bin/bash

#********************
SECONDS=0

source ../../../env.sh
hdfs dfs -rm -r /task3/input/
hdfs dfs -rm -r /task3/output
hdfs dfs -mkdir -p /task3/input/

hdfs dfs -put ./Parking_Violations_Issued_-_Fiscal_Year_2022.csv /task3/input/

/usr/local/spark/bin/spark-submit --conf spark.default.parallelism=2 --master=spark://$SPARK_MASTER:7077 ./task3.py hdfs://$SPARK_MASTER:9000/task2/input/

duration=$SECONDS
duration1=$(($duration % 60))

#********************

SECONDS=0

source ../../../env.sh
hdfs dfs -rm -r /task3/input/
hdfs dfs -rm -r /task3/output
hdfs dfs -mkdir -p /task3/input/

hdfs dfs -put ./Parking_Violations_Issued_-_Fiscal_Year_2022.csv /task3/input/

/usr/local/spark/bin/spark-submit --conf spark.default.parallelism=3 --master=spark://$SPARK_MASTER:7077 ./task3.py hdfs://$SPARK_MASTER:9000/task2/input/

duration=$SECONDS
duration2=$(($duration % 60))

#********************

SECONDS=0

source ../../../env.sh
hdfs dfs -rm -r /task3/input/
hdfs dfs -rm -r /task3/output
hdfs dfs -mkdir -p /task3/input/

hdfs dfs -put ./Parking_Violations_Issued_-_Fiscal_Year_2022.csv /task3/input/

/usr/local/spark/bin/spark-submit --conf spark.default.parallelism=4 --master=spark://$SPARK_MASTER:7077 ./task3.py hdfs://$SPARK_MASTER:9000/task2/input/

duration=$SECONDS
duration3=$(($duration % 60))

#********************

SECONDS=0

source ../../../env.sh
hdfs dfs -rm -r /task3/input/
hdfs dfs -rm -r /task3/output
hdfs dfs -mkdir -p /task3/input/

hdfs dfs -put ./Parking_Violations_Issued_-_Fiscal_Year_2022.csv /task3/input/

/usr/local/spark/bin/spark-submit --conf spark.default.parallelism=5 --master=spark://$SPARK_MASTER:7077 ./task3.py hdfs://$SPARK_MASTER:9000/task2/input/

duration=$SECONDS
duration4=$(($duration % 60))

#********************

echo "time taken with parallelism 2 : $duration1"
echo "time taken with parallelism 3 : $duration2"
echo "time taken with parallelism 4 : $duration3"
echo "time taken with parallelism 5 : $duration4"
