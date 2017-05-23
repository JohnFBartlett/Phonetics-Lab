#! bin/bash

echo Applying creak detection to .wav files in $1
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
			python ~/Desktop/Phonetics_Lab_Work/TextGrid_Scripts/syl_textGrid_maker.py $file
		done
	else
		echo "adjusted"
		for file in $(find . -depth \( -name "*.adjusted*" -o -name "*.phn*" \)); do
			echo converting file $file ...
			VAR=${file##*/}
			python ~/Desktop/Phonetics_Lab_Work/TextGrid_Scripts/adj_textGrid_maker.py $file
		done
	fi
else
	for file in $(find . -depth -name '*.creak'); do
		echo converting file $file ...
		VAR=${file##*/}
		python ~/Desktop/Phonetics_Lab_Work/Task_1_Scripts/creak_textGrid_maker.py $file
	done
fi
