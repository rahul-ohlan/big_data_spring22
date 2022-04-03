#!/bin/bash

centroids=("2.5 5 1" "11 4.5 5" "11 6 11" "25 6.5 14")

start-all.sh

for iter in {0..100}
do

	hadoop dfsadmin -safemode -leave
	
	hadoop fs -rm -r /task2

	hadoop fs -mkdir /task2

	hadoop fs -put ./shot_logs.csv /task2

	hadoop jar /usr/local/hadoop/share/hadoop/tools/lib/hadoop-streaming-3.3.1.jar \
		-file ./bb_mapper.py -mapper ./"bb_mapper.py \"${centroids[0]}\" \"${centroids[1]}\" \"${centroids[2]}\" \"${centroids[3]}\"" \
		-file ./bb_reducer.py -reducer ./bb_reducer.py \
		-input /task2/shot_logs.csv \
		-output /task2/ouptut2

	# now we have our new set of centroids from reducer
	# get that output in a new file
	#hadoop fs -cat /task2/output2/part-00000 > test.txt

	a=("a b c" "d e f" "g h i" "e f g")

	i=0

	hadoop fs -cat /task2/output2/part-00000/ | while read -r line
	do
		a[$i]=$line
		i=$((i+1))

	done
	#done < test.txt

	# now we have our new set of variables in variable a 

	# now checking if they match with the centroids that were input to the mapper

	k=0
	flag="True"

	while [ $k -lt 3 ];
	do
		if [ ["${centroids[$k]}" != "${a[$k]}"] ]
		then
			flag="False"
			break
		fi

		k=$((k+1))

	done

	# now we need to see if match was found or not via the flag variable

	if [ $flag == "False" ]
	then
		k=0
		while [ $k -lt 4 ];
		do
			centroids[$k]=${a[$k]}

			k=$((k+1))

		done

	else
		# if we are inside this else, this means convergence occured
		# we can just break out of for loop now and continue with classification

		break
	fi


done

# now let's begin with the classification
# our final centroids will still be in the centroids variable





# starting the second map reduce phase


hadoop fs jar /usr/local/hadoop/share/hadoop/tools/lib/hadoop-streaming-3.3.1.jar \
	-file ./bb_mapaper2.py -mapper ./"bb_mapper.py \"${centroids[0]}\" \"${centroids[1]}\" \"${centroids[2]}\" \"${centroids[3]}\"" \
	-file ./bb_reducer2.py -reducer ./ bb_reducer2.py \
	-input /task2/shot_logs.csv \
	ouptut /task2/output3


# now print the final output on terminal

hadoop fs -cat /task2/output3/part-0000

# now clean the hdfs file system

hadoof fs -rm -r /task2


stop-all.sh
