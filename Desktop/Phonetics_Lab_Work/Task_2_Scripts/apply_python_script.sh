#! bin/bash

# take in and interpret arguments
if [ $# -le 1 ]; then 
	# give directions
    if [[ $1 == "-help" ]]; then
    	echo
    	echo "This script takes in a python script (first argument) and applies it to a given directory or file (second argument)."
    	echo
    	echo "An output directory and/or file type to use within the given directory are optionally taken in as additional arguments."
    	echo "To supply output directory, enter -o (directory) with space separation."
    	echo "To supply file type, enter -t (type) with space separation."
    	echo "Example file types are 'wav', 'txt', 'TextGrid', etc."
    	echo
    	exit
   	else
    	echo "Need at least python script name and input directory/file"
    	echo "Type bash apply_python_script -help for more directions."
    	exit
    fi
else 
# at least two arguments
	# check that first argument is a python script
	if [[ $1 != *".py" ]]; then
		echo "Specify script as first argument (must end in .py)."
		echo "Type bash apply_python_script -help for more directions."
		exit
	fi
	# check that second argument is a file or directory
	if [ ! -f $2 ]; then
		if [ ! -d $2 ]; then
			echo "Second argument is not a found file or directory."
			echo "Type bash apply_python_script -help for more directions."
			exit
		fi
	fi
fi
if [[ $# == 2 ]]; then 
	if [[ $TYPE == "f" ]]; then
	#input is one file
		python $1 $2
		exit
	else
	#input is directory
		for file in $2; do
			python $1 $file
		done
		exit
	fi
# see if optional arguments given
elif [ $# -le 6 ]; then
	#first find out what $3 is
	if [[ $3 == "-o" ]]; then
		# output specified
		if [ $# -le 3 ]; then
			echo "No output path given!"
			echo "Type bash apply_python_script -help for more directions."
			exit
		fi
		
		#check if additional argument given
		if [ $# -ge 5 ]; then
			if [[ $5 == "-t" ]]; then
				# type specified
				if [[ $# == 5 ]]; then
					echo "No type given!"
					echo "Type bash apply_python_script -help for more directions."
					exit
				fi

				# run given arguments
				if [[ $TYPE == "f" ]]; then
				#input is one file
					#check if file is correct type
					if $6 in $2; then
						python $1 $2 $4
						exit
					else 
						echo "File is not of the correct type!"
						echo "Type bash apply_python_script -help for more directions."
						exit
					fi
				else
				#input is directory
					# apply for all files of correct type
					for file in $(find $2 -name *$6); do
						python $1 $file $4
					done
					exit
				fi
			else 
				echo "Already sepcified output. Only other option is type (-t)."
				echo "Type bash apply_python_script -help for more directions."
				exit
			fi
		# otherwise run given arguments
		else 
			# run given arguments
			if [[ $TYPE == "f" ]]; then
				#input is one file
				python $1 $2 $4
				exit
			else
			#input is directory
				# apply for all files of correct type
				for file in $2; do
					python $1 $file $4
				done
				exit
			fi
		fi 
	elif [[ $3 == "-t" ]]; then
		if [[ $# == 3 ]]; then
			echo "No type given!"
			echo "Type bash apply_python_script -help for more directions."
			exit
		fi
		
		#check if additional argument given
		if [ $# -ge 5 ]; then
			if [[ $5 == "-o" ]]; then
				# output specified
				if [[ $# == 5 ]]; then
					echo "No output path given!"
					echo "Type bash apply_python_script -help for more directions."
					exit
				fi
				
				# run given arguments
				if [[ $TYPE == "f" ]]; then
				#input is one file
					#check if file is correct type
					if $4 in $2; then
						python $1 $2 $6
						exit
					else 
						echo "File is not of the correct type!"
						echo "Type bash apply_python_script -help for more directions."
						exit
					fi
				else
				#input is directory
					# apply for all files of correct type
					for file in $(find $2 -name *$4); do
						python $1 $file $6
					done
					exit
				fi
			else 
				echo "Already sepcified type. Only other option is output (-o)."
				echo "Type bash apply_python_script -help for more directions."
				exit
			fi
		# otherwise run given arguments
		else
			if [[ $TYPE == "f" ]]; then
			#input is one file
				#check if file is correct type
				if $4 in $2; then
					python $1 $2
					exit
				else 
					echo "File is not of the correct type!"
					echo "Type bash apply_python_script -help for more directions."
					exit
				fi
			else
			#input is directory
				for file in $(find $2 -name *$4); do
					python $1 $file
				done
				exit
			fi
		fi
	else 
		echo "Must specify -o or -t before optional arguments."
		echo "Type bash apply_python_script -help for more directions."
		exit
	fi
else
	echo "Too many arguments: "$#
	echo "Type bash apply_python_script -help for more directions."
	exit
fi
