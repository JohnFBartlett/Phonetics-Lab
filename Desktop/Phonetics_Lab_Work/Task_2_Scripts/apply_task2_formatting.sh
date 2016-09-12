#! bin/bash

if ! "COSPRO_0" in $1 then
	echo "Directory argument must be a COSPRO corpus!"

else
	echo Applying task 2 formatting to files in $1
	cd ~/Desktop/COSPRO_DATA_BIN/Task2_Formatting

	for file in ./1-Segments/$1/*; do
		echo executing file $file ...
		# VAR=${file%.*}
		ADJ=${file##*/}
		NAME=${ADJ%.*}
		# check if each folder exists, assign N/A if not
		if [ -d './2-Formatted_Break/'$1'/'$NAME'.break_f' ]; then
			BREAK='./2-Formatted_Break/'$1'/'$NAME'.break_f'
		else
			BREAK='N/A'
		fi
		if [ -d './2-Formatted_Measures/'$1'/'$NAME'.measures_aligned' ]; then
			MEAS='./2-Formatted_Measures/'$1'/'$NAME'.measures_aligned'
		else 
			MEAS='N/A'
		fi
		if [ -d './2-Formatted_Creak/'$1'/'$NAME'.creak_aligned' ]; then
			CREAK='./2-Formatted_Creak/'$1'/'$NAME'.creak_aligned'
		else 
			CREAK='N/A'
		fi
		if [ -d './2-Formatted_Reaper_Results/'$1'/'$NAME'.f0_aligned' ]; then
			REAP='./2-Formatted_Reaper_Results/'$1'/'$NAME'.f0_aligned'
		else 
			REAP='N/A'
		fi
		# echo name $NAME
		# echo adj $ADJ
		# echo brk $BREAK
		# echo meas $MEAS
		python ~/Desktop/Phonetics_Lab_Work/Task_2_Scripts/format_for_Task2_sheet.py $file $BREAK $CREAK $REAP $MEAS ./3-Combined/$1/
	done
fi