#! bin/bash

if [[ "$1" == *"COSPRO_0"* ]] || [[ "$1" == *"Child"* ]] ; then
	echo Applying task 2 formatting to files in $1
	cd ~/Documents/Phonetics_Lab_Summer_2017/Phonetics-Lab/COSPRO_DATA_BIN/data_analysis/
	PLACE='./2-Formatted_Segments/'$1

	pwd
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
		python2.6 ~/Documents/Phonetics_Lab_Summer_2017/Phonetics-Lab/FULL_PROCEDURE/Section-1_making_COSPRO_Dataset/Phase-6_\(Create_Combined_Dataset\)/format_for_Task2_sheet.py $file $BREAK $CREAK $REAP $MEAS ./3-Combined/$1
	done
	for file in $PLACE*.phn_fixed; do
		# echo "=======================FILESTART=============="
		if [ -f $file ]; then
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
			python2.6 ~/Documents/Phonetics_Lab_Summer_2017/Phonetics-Lab/FULL_PROCEDURE/Section-1_\(Create_Main_Dataset_for_COSPRO_corpora\)/Phase-6_\(Create_Combined_Dataset\)/format_for_Task2_sheet.py/format_for_Task2_sheet.py $file $BREAK $CREAK $REAP $MEAS ./3-Combined/$1/
		fi
	done
else
	echo "Directory argument must be a COSPRO corpus!"

fi