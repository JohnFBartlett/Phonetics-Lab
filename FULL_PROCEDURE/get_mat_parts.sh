#! bin/bash

echo Combining .mat files in $1
cd $1
if ! [ -d Output ]
then
	mkdir Output
fi

pwd

for file in $(find . -depth -name '*.mat'); do
	# only do this for the first part of each group
	# echo found one
	if [[ $file == *"part00"* ]]
	then
		# get name
		VAR=${file%part00.*}
		VAR=${VAR##*/}
		echo combining file $VAR ...
		matlab -nodesktop -nosplash -nojvm -r "name = '$VAR'; combine_mat_parts(name); quit"
	fi
done