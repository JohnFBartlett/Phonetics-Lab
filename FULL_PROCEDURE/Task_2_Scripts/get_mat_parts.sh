#! bin/bash

if [ $2 = "fix" ]; 
	then
	echo fixing .mat files in $1
	cd $1
	if ! [ -d Output ]
	then
		mkdir Output
	fi
	
	pwd
	for file in $(find . -depth -name '*.mat'); do
		# only do this for the first part of each group
		echo "found " $file
		# get name
		VAR=${file##*/}
		echo fixing file $VAR ...
		matlab -nodesktop -nosplash -nojvm -r "name = '$VAR'; fix_mat_parts(name); quit"
	done

else
	echo Combining .mat files in $1
	cd $1
	if ! [ -d Output ]
	then
		mkdir Output
	fi
	
	pwd
	
	for file in $(find . -depth -name '*.mat'); do
		# only do this for the first part of each group
		echo "found " $file
		if [[ $file == *"part00"* ]]; 
		then
			# get name
			VAR=${file%part00.*}
			VAR=${VAR##*/}
			echo combining file $VAR ...
			matlab -nodesktop -nosplash -nojvm -r "name = '$VAR'; combine_mat_parts(name); quit"
		fi
	done
fi