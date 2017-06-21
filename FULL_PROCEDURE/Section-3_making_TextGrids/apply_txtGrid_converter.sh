#! bin/bash

echo Creating TextGrids from files in $1
cd $1

pwd

if ! [ -z "$2" ]
	then
	if [ "$2" == "-s" ]; 
		then
		echo "syl"
		for file in $(find . -depth -name '*.syl'); do
			echo converting file $file ...
			VAR=${file##*/}
			python2.6 ~/Documents/Phonetics_Lab_Summer_2017/Phonetics-Lab/FULL_PROCEDURE/Section-3_making_TextGrids/syl_textGrid_maker.py $file
		done
	else
		echo "adjusted"
		for file in $(find . -depth \( -name "*.adjusted*" -o -name "*.phn*" \)); do
			echo converting file $file ...
			VAR=${file##*/}
			python2.6 ~/Documents/Phonetics_Lab_Summer_2017/Phonetics-Lab/FULL_PROCEDURE/Section-3_making_TextGrids/adj_textGrid_maker.py $file
		done
	fi
else
	for file in $(find . -depth -name '*.creak'); do
		echo converting file $file ...
		VAR=${file##*/}
		python2.6 ~/Documents/Phonetics_Lab_Summer_2017/Phonetics-Lab/FULL_PROCEDURE/Section-3_making_TextGrids/creak_textGrid_maker.py $file
	done
fi
