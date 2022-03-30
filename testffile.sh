#!/bin/bash



centroids=("2 4 5" "5 6 7" "9 8 3")

python verstappen.py "${centroids[0]}" "${centroids[1]}"
a=("a b c" "d e f" "g H i")
i=0
while read -r line       # taking the data of reducer output in an array variable
do
        echo $i
        echo $line
        a[$i]=$line
        i=$((i+1))
done < test.txt

echo ${a[*]}

k=0
flag="True"

while [ $k -lt 3 ]; do

        if [ ["${centroids[$k]}" != "${a[$k]}"] ]
        then
                flag="False"
                break
        fi

        k=$((k+1))

done


if [ $flag == "False" ]
then
        k=0
        while [ $k -lt 3 ]; do
                centroids[$k]=${a[$k]}

                k=$((k+1))
        done
fi

echo "this is new centroid rahul"
echo ${centroids[*]}

# now a has our new centroids from reducer
# need to compare them with previous centroids
# is same, break out of loop
# if not update centroids
1,11          Top
