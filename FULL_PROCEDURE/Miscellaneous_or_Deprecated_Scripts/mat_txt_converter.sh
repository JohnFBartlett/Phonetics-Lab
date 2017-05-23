#! bin/bash

echo Converting .mat files to .txt files in $1
cd $1
if [ -d txt_Output ] 
then
	echo deleting old txt_Output folder
	rmdir txt_Output
fi

pwd

mkdir txt_Output
for file in $(find . -name '*.wav'); do
	# echo executing file $file ...
	VAR=${file%.*}
	VAR=${VAR##*/}
	matlab -nodesktop -nosplash -nojvm -r "file = '$VAR.mat'; load('file'); dlmwrite('$VAR.txt', file, 'delimiter','\t'); quit"
done