#! bin/bash

if [[ "$1" == *"COSPRO_0"* ]]; then
	echo Applying task 2 formatting to files in $1
	cd ~/Desktop/COSPRO_DATA_BIN/Task2_Formatting
	PLACE='./2-Formatted_Segments/'$1

	echo "=======================BEGINNING=============="
	if [ -d "$PLACE" ]; then 
		echo "this directory does exist"
	fi
	for file in $PLACE*.adjusted_fixed; do
		# echo "=======================FILESTART=============="
		echo executing file $file ...
		# VAR=${file%.*}
		ADJ=${file##*/}
		NAME=${ADJ%.*}
		# check if each folder exists, assign N/A if not
		if [ -f './2-Formatted_Break/'$1$NAME'.break_fixed' ]; then
			BREAK='./2-Formatted_Break/'$1$NAME'.break_fixed'
		else
			BREAK='N/A'
			# echo brk $BREAK
		fi
		if [ -f './2-Formatted_Measures/'$1$NAME'.measures_aligned' ]; then
			MEAS='./2-Formatted_Measures/'$1$NAME'.measures_aligned'
		else 
			MEAS='N/A'
			# echo meas $MEAS
		fi
		if [ -f './2-Formatted_Creak/'$1$NAME'.creak_aligned' ]; then
			CREAK='./2-Formatted_Creak/'$1$NAME'.creak_aligned'
		else 
			CREAK='N/A'
			# echo creak $REAP
		fi
		if [ -f './2-Formatted_Reaper_Results/'$1$NAME'.f0_aligned' ]; then
			REAP='./2-Formatted_Reaper_Results/'$1$NAME'.f0_aligned'
		else 
			REAP='N/A'
			# echo reaper $REAP
		fi
		# echo name $NAME
		# echo adj $ADJ
		# echo brk $BREAK
		# echo creak $CREAK
		# echo reaper $REAP
		# echo meas $MEAS
		python ~/Desktop/Phonetics_Lab_Work/Task_2_Scripts/format_for_Task2_sheet.py $file $BREAK $CREAK $REAP $MEAS ./3-Combined/$1/
	done
	for file in $PLACE*.phn_fixed; do
		# echo "=======================FILESTART=============="
		echo executing file $file ...
		# VAR=${file%.*}
		ADJ=${file##*/}
		NAME=${ADJ%.*}
		# check if each folder exists, assign N/A if not
		if [ -f './2-Formatted_Break/'$1$NAME'.break_fixed' ]; then
			BREAK='./2-Formatted_Break/'$1$NAME'.break_fixed'
		else
			BREAK='N/A'
			echo brk $BREAK
		fi
		if [ -f './2-Formatted_Measures/'$1$NAME'.measures_aligned' ]; then
			MEAS='./2-Formatted_Measures/'$1$NAME'.measures_aligned'
		else 
			MEAS='N/A'
			echo meas $MEAS
		fi
		if [ -f './2-Formatted_Creak/'$1$NAME'.creak_aligned' ]; then
			CREAK='./2-Formatted_Creak/'$1$NAME'.creak_aligned'
		else 
			CREAK='N/A'
			echo creak $REAP
		fi
		if [ -f './2-Formatted_Reaper_Results/'$1$NAME'.f0_aligned' ]; then
			REAP='./2-Formatted_Reaper_Results/'$1$NAME'.f0_aligned'
		else 
			REAP='N/A'
			echo reaper $REAP
		fi
		echo name $NAME
		echo adj $ADJ
		echo brk $BREAK
		echo creak $CREAK
		echo reaper $REAP
		echo meas $MEAS
		python ~/Desktop/Phonetics_Lab_Work/Task_2_Scripts/format_for_Task2_sheet.py $file $BREAK $CREAK $REAP $MEAS ./3-Combined/$1/
	done
else
	echo "Directory argument must be a COSPRO corpus!"

fi