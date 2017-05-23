#! bin/bash

echo Applying textGrid labeling to .TextGrid files in $1
cd $1

pwd

for file in $(find . -depth -name '*.TextGrid'); do
	echo converting file $file ...
	VAR=${file##*/}
	python ~/Desktop/Phonetics_Lab_Work/TextGrid_Scripts/textGrid_labeler.py $file SVO_Chinese_words_and_sentences.csv
done