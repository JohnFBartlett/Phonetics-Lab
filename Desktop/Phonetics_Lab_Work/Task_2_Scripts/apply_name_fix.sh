#!/bin/bash

for f in $1/*; do
	VALUE=`python ~/Desktop/Phonetics_Lab_Work/Task_2_Scripts/fix_part_names.py $f`
	
	mv $f $VALUE

done
