#!/bin/bash

centroids=("34930 11110 0" "35170 13610 10910" "35290 11710 10810" "34810 14510 15710" "34890 10810 44990" "34790 4081 14510" "35230 14190 1110")

start-all.sh

hdfs dfsadmin -safemode leave

hadoop fs -rm -r /task2
hadoop fs -mkdir /task2
hadoop fs -put ./Parking_Violations_Issued_-_Fiscal_Year_2022.csv /task2

for iter in {0..100};
do



	hdfs dfsadmin -safemode leave
	echo "iteration number : $iter "
	echo " input centroids : ${centroids[*]} "
	


	hadoop jar /usr/local/hadoop/share/hadoop/tools/lib/hadoop-streaming-3.3.1.jar \
		-file ./mapper.py -mapper ./"mapper.py \"${centroids[0]}\" \"${centroids[1]}\" \"${centroids[2]}\" \"${centroids[3]}\" \"${centroids[4]}\" \"${centroids[5]}\" \"${centroids[6]}\"" \
		-file ./reducer.py -reducer ./reducer.py \
		-input /task2/Parking_Violations_Issued_-_Fiscal_Year_2022.csv \
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
	-file ./mapper2.py -mapper ./"mapper2.py \"${centroids[0]}\" \"${centroids[1]}\" \"${centroids[2]}\" \"${centroids[3]}\" \"${centroids[4]}\" \"${centroids[5]}\" \"${centroids[6]}\"" \
	-file ./reducer2.py -reducer ./reducer2.py \
	-input /task2/Parking_Violations_Issued_-_Fiscal_Year_2022.csv \
	-output /task2/output3


# now print the final output on terminal

hadoop fs -cat /task2/output3/part-00000

# now clean the hdfs file system

hadoop fs -rm -r /task2


stop-all.sh