#! bin/bash

echo Applying reaper analysis to .wav files in $1
cd $1

# if [ -d Reaper_Analysis ] 
# then
# 	echo deleting old Reaper_Analysis folder
# 	rmdir Reaper_Analysis
# fi

# pwd

# mkdir Reaper_Analysis

for file in $(find . -type f -name '*.wav'); do
	echo executing on file $file ...
	VAR=${file%.*}
	CUT=${VAR##*/}
	# ~/Desktop/Phonetics_Lab_Work/REAPER_repo/REAPER/build/reaper -i $VAR.wav -f ~/Desktop/COSPRO_DATA_BIN/Reaper_Results/$CUT.f0 -p ~/Desktop/COSPRO_DATA_BIN/Reaper_Results/$CUT.pm -a
	# ~/Desktop/Phonetics_Lab_Work/REAPER_repo/REAPER/build/reaper -i $VAR.wav -p ~/Desktop/COSPRO_DATA_BIN/Reaper_Results/$CUT.pm -a
	~/Desktop/Phonetics_Lab_Work/REAPER_repo/REAPER/build/reaper -i $VAR.wav -f ~/Desktop/COSPRO_DATA_BIN/Task2_Formatting/$CUT.f0 -p ~/Desktop/COSPRO_DATA_BIN/Task2_Formatting/$CUT.pm -a
done