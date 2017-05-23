#! bin/bash

echo Applying creak detection to .wav files in $1
cd $1
if ! [ -d Output ]
then
	mkdir Output
fi

pwd

for file in $(find . -name '*.wav'); do
	echo executing file $file ...
	VAR=${file%.*}
	VAR=${VAR##*/}
	matlab -nodesktop -nosplash -nojvm -r "file = '$VAR'; make_file_for_creakyDetection(file); quit"
done