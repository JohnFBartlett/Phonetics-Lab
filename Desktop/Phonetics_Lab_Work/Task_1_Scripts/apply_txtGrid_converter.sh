#! bin/bash

echo Applying creak detection to .wav files in $1
cd $1

pwd

for file in $(find . -name '*.txt'); do
	echo converting file $file ...
	VAR=${file##*/}
	python textGrid_maker.py $file
done