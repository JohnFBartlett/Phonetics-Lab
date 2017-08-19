#! bin/bash
cd ~/Documents/Phonetics_Lab_Summer_2017/Phonetics-Lab/COSPRO_DATA_BIN/data_analysis/

for file in $(find adj_TextGrids/ -depth -type f -name "*TextGrid"); do
	 
	# ADJ=${file##*/}
	NAME=${file##*/}
    echo -ne '\r'
	echo -n $NAME'... '
	if [ -f './creak_TextGrids/'$NAME ]; then
		CREAK='./creak_TextGrids/'$NAME
		python ~/Documents/Phonetics_Lab_Summer_2017/Phonetics-Lab/FULL_PROCEDURE/Section-3_making_TextGrids/combined_creak_and_segment $file $CREAK
	fi
done
