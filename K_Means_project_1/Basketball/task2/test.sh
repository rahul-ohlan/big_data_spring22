#!/bin/bash

centroids=("2.5 5 1" "11 4.5 5" "11 6 11" "25 6.5 14")

start-all.sh

hdfs dfsadmin -safemode leave

hadoop fs -rm -r /task2
hadoop fs -mkdir /task2
hadoop fs -put ./shot_logs.csv /task2

for iter in {0..100};
do



	hdfs dfsadmin -safemode leave
	echo "iteration number : $iter "
	echo " input centroids : ${centroids[*]} "
	


	hadoop jar /usr/local/hadoop/share/hadoop/tools/lib/hadoop-streaming-3.3.1.jar \
		-file ./bb_mapper.py -mapper ./"bb_mapper.py \"${centroids[0]}\" \"${centroids[1]}\" \"${centroids[2]}\" \"${centroids[3]}\"" \
		-file ./bb_reducer.py -reducer ./bb_reducer.py \
		-input /task2/shot_logs.csv \
		-output /task2/output2


	hadoop fs -cat /task2/output2/part-00000 > test.txt

	flag="False"
	i=0

	while IFS= read -r line;
	do
		if [ "${centroids[$i]}" != "$line" ];
		then
			flag="True"
			echo "mismatch found at $i"
			echo "breaking out of loop to update centroids"
			break
		fi

		i=$((i+1))

	done < test.txt
	
	if [ "$flag" = "False" ];
	then
		# match was found
		echo "congrats! match was found"
		echo "breaking out of the FOR loop " 
		echo " new final centroids are : ${centroids[*]}"
		break

	else

		k=0
		while IFS= read -r line;
		do
			
			echo "updating centroid at $k"
			centroids[$k]="$line"
			k=$((k+1))


		done < test.txt

		echo " new centroids : ${centroids[*]} "

	fi

	hadoop fs -rm -r /task2/output2


done


# now let's begin with the classification
# our final centroids will still be in the centroids variable


hadoop fs -rm -r /task2
hadoop fs -mkdir /task2
hadoop fs -put ./shot_logs.csv /task2
hdfs dfsadmin -safemode leave

# starting the second map reduce phase


hadoop jar /usr/local/hadoop/share/hadoop/tools/lib/hadoop-streaming-3.3.1.jar \
	-file ./bb_mapper2.py -mapper ./"bb_mapper2.py \"${centroids[0]}\" \"${centroids[1]}\" \"${centroids[2]}\" \"${centroids[3]}\"" \
	-file ./bb_reducer2.py -reducer ./bb_reducer2.py \
	-input /task2/shot_logs.csv \
	-output /task2/output3


# now print the final output on terminal

hadoop fs -cat /task2/output3/part-00000

# now clean the hdfs file system

hadoop fs -rm -r /task2


stop-all.sh
