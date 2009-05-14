#!/bin/sh

# quick & dirty to get answers 
# might need change cookie values

user="xxxx"
key="yyyy"

for x in `seq 1 244`
do
	wget -q --no-cookies --header "Cookie: p_username=$user;p_key=$key" "http://projecteuler.net/index.php?section=problems&id=$x" -O $x
	a=`grep -A 2 Answer  $x|tail -1|sed -e 's/^.*<b>//' -e 's/<.*$//'`
	echo "$x: $a"
	sleep 5
done
