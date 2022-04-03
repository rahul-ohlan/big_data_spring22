#!/usr/bin/bash

centroids=("2.5 5 1" "11 4.5 5" "11 6 11" "25 6.5 14")
random=("2.5 5 1" "11 4 5" "11 6 11" "25 6.5 14")


k=0
while [ $k -lt 4 ];
do
	if [ "${centroids[$k]}" != "${random[$k]}" ];
	then
		echo $k
		echo " difference found, breaking out of loop"
		break

	else
		echo "match found"
		echo ${centroids[$k]}

	fi

	k=$((k+1))


done
exit 0

