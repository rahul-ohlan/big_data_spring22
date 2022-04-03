#!/bin/bash

centroids=("2.5 5 1" "11 4.5 5" "11 6 11" "25 6.5 14")

start-all.sh

hadoop dfsadmin -safemode -leave

hadoop fs -rm -r /task2
hadoop fs -mkdir /task2
hadoop fs -put ./shot_logs.csv /task2

for iter in {0..100};
do



	hadoop dfsadmin -safemode -leave
	
	hadoop fs -rm -r /task2/output2


	hadoop jar /usr/local/hadoop/share/hadoop/tools/lib/hadoop-streaming-3.3.1.jar \
		-file ./bb_mapper.py -mapper ./"bb_mapper.py \"${centroids[0]}\" \"${centroids[1]}\" \"${centroids[2]}\" \"${centroids[3]}\"" \
		-file ./bb_reducer.py -reducer ./bb_reducer.py \
		-input /task2/shot_logs.csv \
		-output /task2/ouptut2


	hadoop fs -cat /task2/output2/part-00000/ > test.txt

	flag="False"
	i=0

	while IFS= read -r line;
	do
		if [ "${centroids[$i]}" != "$line" ];
		then
			flag="True"
			break
		fi

		i=$((i+1))

	done < test.txt
	
	if [ "$flag" = "False" ];
	then
		# match was found
		break

	else

		k=0
		while IFS= read -r line;
		do
			centroids[$k]="$line"
			k=$((k+1))

		done < test.txt

	fi


done


# now let's begin with the classification
# our final centroids will still be in the centroids variable





# starting the second map reduce phase


hadoop fs jar /usr/local/hadoop/share/hadoop/tools/lib/hadoop-streaming-3.3.1.jar \
	-file ./bb_mapper2.py -mapper ./"bb_mapper2.py \"${centroids[0]}\" \"${centroids[1]}\" \"${centroids[2]}\" \"${centroids[3]}\"" \
	-file ./bb_reducer2.py -reducer ./ bb_reducer2.py \
	-input /task2/shot_logs.csv \
	ouptut /task2/output3


# now print the final output on terminal

hadoop fs -cat /task2/output3/part-0000

# now clean the hdfs file system

hadoof fs -rm -r /task2


stop-all.sh
