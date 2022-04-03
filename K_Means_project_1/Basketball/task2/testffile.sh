#!/bin/bash



centroids=("2.5 5 1" "11 4.5 5" "11 6 11" "25 6.5 14")

for iter in {0..100};
do


	flag="False"
	i=0

	echo "iteration number $iter : "
	echo " input centroids: ${centroids[*]} "
	cat shot_logs.csv | python bb_mapper.py "${centroids[0]}" "${centroids[1]}" "${centroids[2]}" "${centroids[3]}" | sort | python bb_reducer.py > test.txt

	while IFS= read -r line;
	do
		if [ "${centroids[$i]}" != "$line" ];
		then
			echo $i
			echo "mismatch found"
			echo "breaking out of loop right here"
			flag="True"
			break

		fi

		i=$((i+1))

	done < test.txt

	if [ "$flag" = "False" ];
	then
	# it means match was found, then no need to do any further iteration
	# and take the centroids as it is

		echo " Congrats! Match was found"
		echo "breaking out of the for loop"
		break

	else
		# else, it means need to update the centroids
		k=0
		while IFS= read -r line;
		do
			centroids[$k]="$line"
			echo $k
			echo "centroids at $k updated"
			k=$((k+1))

		done < test.txt
	fi



done

echo "these are new centroids Rahul"
echo ${centroids[*]}



# now a has our new centroids from reducer
# need to compare them with previous centroids
# is same, break out of loop
# if not update centroids
