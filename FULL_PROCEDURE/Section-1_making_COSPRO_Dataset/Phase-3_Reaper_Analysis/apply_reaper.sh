#! bin/bash

echo Applying reaper analysis to .wav files in $1
cd $1

if [ -d Output ] 
then
	echo deleting old Output folder
	rm -r Output/
fi

mkdir Output

for file in $(find . -type f -name '*.wav'); do
	echo executing on file $file ...
	VAR=${file%.*}
	CUT=${VAR##*/}
	# ~/Desktop/Phonetics_Lab_Work/REAPER_repo/REAPER/build/reaper -i $VAR.wav -f ~/Desktop/COSPRO_DATA_BIN/Reaper_Results/$CUT.f0 -p ~/Desktop/COSPRO_DATA_BIN/Reaper_Results/$CUT.pm -a
	# ~/Desktop/Phonetics_Lab_Work/REAPER_repo/REAPER/build/reaper -i $VAR.wav -p ~/Desktop/COSPRO_DATA_BIN/Reaper_Results/$CUT.pm -a
	~/Documents/Phonetics_Lab_Summer_2017/Phonetics-Lab/ONLY_LOCAL/REAPER_repo/REAPER/build/reaper -i $VAR.wav -f ~/Desktop/COSPRO_DATA_BIN/Task2_Formatting/1-Raw_Reaper_Results/$CUT.f0 -a
done