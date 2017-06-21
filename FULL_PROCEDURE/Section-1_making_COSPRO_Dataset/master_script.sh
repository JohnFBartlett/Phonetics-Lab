#! bin/bash

# Sample execution:
# plab -b Section-1_making_COSPRO_Dataset/master_script.sh {CORPUS NAME}
echo "----------------------------------------------------------------"
echo "Beginning Phonetics Lab data analysis procedure on corpus $1"

cd ~/Documents/Phonetics_Lab_Summer_2017/Phonetics-Lab/COSPRO_DATA_BIN/data_analysis/0-Base_Files/

cd $1 || echo "$1 does not exist in directory 0-Base_Files/"


# Ask about Phase 1: Initial Steps
echo
echo -n "What type of files should be analyzed?(phr/prg/w/all/etc) "
read type

echo
echo -n "Are Initial Steps completed?(y/n) "
read yn
if [[ "$yn" =~ ^(n|N|no|No) ]]; then
	echo
	echo -n "Are spaces removed?(y/n) "
	read yn
	if [[ "$yn" =~ ^(n|N|no|No) ]]; then
		echo "Removing spaces from filenames in corpus..."
		for f in $(find . -type f); do
			mv "${f}" "${f// /_}" 
		done
	fi

    # Ask if break files need to be formatted
	echo
	echo -n "Have break files been formatted?(y/n) "
	if [[ "$yn" =~ ^(n|N|no|No) ]]; then
		echo "Moving break files and removing carriage returns..."
		for file in $(find . -type f -name "*${type}*.break"); do
		    tr -d "\015" <file1
		    cp ${file} ../../2-Formatted_Break/$1 || echo "Could not find ../../2-Formatted_Break/$1" | pwd
		done
	fi

	# Ask if adjusted files need to be formatted
    echo
    echo -n "Have adjusted/phn files been formatted?(y/n)"
    read yn
    if [[ "$yn" =~ ^(n|N|no|No) ]]; then
        echo "Moving adjusted files and removing carriage returns..."
		for file in $(find . -type f -name "*${type}*.adjusted"); do
		    tr -d "\015" <file1
		    cp ${file} ../../2-Formatted_Adjusted/$1 || echo "Could not find ../../2-Formatted_Adjusted/$1" | pwd
		done
		echo "Moving phn files and removing carriage returns..."
		for file in $(find . -type f -name "*${type}*.phn"); do
		    tr -d "\015" <file1
		    cp ${file} ../../2-Formatted_Adjusted/$1 || echo "Could not find ../../2-Formatted_Adjusted/$1" | pwd
		done
    fi

	# After all initial steps completed
	echo "Initial steps completed."
	echo
	echo -n "Continue?(y/n) "
	read yn
	if [[ "$yn" =~ ^(y|Y|yes|Yes) ]]; then
		exit 1
	fi
fi

# Ask about Phase 4: VoiceSauce Analysis
echo
echo -n "Has VoiceSauce been run, or is it being run, on desired wav files?(y/n) "
read yn
if [[ "$yn" =~ ^(n|N|no|No) ]]; then
	echo "Are desired wav files in a single folder?(y/n) "
	read yn
	if [[ "$yn" =~ ^(n|N|no|No) ]]; then
		echo "Preparing to create folder for all desired wav files..."

		if [[ ${type} == "" ]]; then
			mkdir all_wav/
			find . -name "*.wav" -exec cp {} ./all_wav \;
			echo "Starting Matlab in background. Please execute VoiceSauce on ./all_wav and then return to prompt"
			matlab &
		else
			mkdir ${type}"_wav"
			find . -name "*${type}*.wav" -exec cp {} "./${type}_wav" \;
			echo "Starting Matlab. Please execute VoiceSauce on folder ./"${type}"_wav"
			matlab &
		fi
	else
		echo "Starting Matlab in background. Please execute VoiceSauce on desired folder and then return to prompt"
		matlab &
	echo -n "Continue?(y/n)"
	read yn
	if [[ "$yn" =~ ^(n|N|no|No) ]]; then
	    quit 0
	fi
	echo "Continuing while Matlab runs in background..."
	fi
fi

# Ask about Phase 2: Creak Analysis
echo
echo -n "Has Creak detection been run, or is it being run, on desired files?(y/n)"
read yn
if [[ "$yn" =~ ^(n|N|no|No) ]]; then
    if [ ! -d "Voice_Analysis_Toolkit-master" ]; then
        cp ~/Documents/Phonetics_Lab_Summer_2017/Phonetics-Lab/FULL_PROCEDURE/Section-1_making_COSPRO_Dataset/Phase-2_Creak_Analysis/VoiceSauce_Analysis_Toolkit-master .
    fi
    plab -b Section-1_making_COSPRO_Dataset/Phase-2_Creak_Analysis/apply_creak_detection.sh .
    find ./Output/ -name *creak -exec mv {} ../../1-Raw_Creak/$1
fi

echo -n "Continue?(y/n)"
read yn
if [[ "$yn" =~ ^(n|N|no|No) ]]; then
    quit 0
fi

# Ask about Phase 3: Reaper Analysis
echo
echo -n "Has Reaper analysis been run, or is it being run, on desired files?(y/n)"
read yn
if [[ "$yn" =~ ^(n|N|no|No) ]]; then
    plab -b Section-1_making_COSPRO_Dataset/Phase-3_Reaper_Analysis/apply_reaper .
    find ./Output/ -name *creak -exec mv {} ../../1-Raw_Reaper/$1
fi

echo -n "Continue?(y/n)"
read yn
if [[ "$yn" =~ ^(n|N|no|No) ]]; then
    quit 0
fi

__ DONE THROUGH HERE ___

# Ask about Phase 5: File Alignment
echo
echo "Checking for adjusted files..."
# Check reaper
if [[ -n "$(ls ../../2-Formatted_Adjusted)" ]]; then
    echo "Found adjusted/phn files"
else
    echo "No files found in ../../2-Formatted_Adjusted! Cannot format other files without .adjusted or .phn files"
fi

# Check reaper
echo "Formatting raw reaper files"
if [[ -n "$(ls ../../1-Raw_Reaper)" ]]; then
    echo "Found files in Raw Reaper folder"
    plab -p Section-1_making_COSPRO_Dataset/Phase-5_Align_Files/convert_to_15_intervalsV2.py reaper $1 10
else
    echo "No files found in ../../1-Raw_Reaper!"
fi

# Check creak
echo "Formatting raw creak files"
if [[ -n "$(ls ../../1-Raw_Creak)" ]]; then
    echo "Found files in Raw Creak folder"
    plab -p Section-1_making_COSPRO_Dataset/Phase-5_Align_Files/convert_to_15_intervalsV2.py creak $1 10
else
    echo "No files found in ../../1-Raw_Creak!"
fi

echo
echo -n "Have VoiceSauce files been split into segments?(y/n)"
read yn
if [[ "$yn" =~ ^(n|N|no|No) ]]; then
    plab -p Section-1_making_COSPRO_Dataset/Phase-5_Align_Files/split_measures.py ../../1-Raw_Measures/$1 ../../2-Formatted_Measures/$1
fi

echo
echo -n "Files formatted. Continue?(y/n)"
read yn
if [[ "$yn" =~ ^(n|N|no|No) ]]; then
    quit 0
fi

# Do Phase 6: Create combined Dataset
echo "Creating combined dataset"

# Run task2_formatting
plab -b Section-1_making_COSPRO_Dataset/Phase-6_Create_Combined_Dataset/apply_task2_formatting.sh $1

# Go into parts and combine tables
plab -p Section-1_making_COSPRO_Dataset/Phase-6_Create_Combined_Dataset/combine_tables.py ../../3-Combined/${1}parts/ ${1}_combined.txt

# Move combined file out of the parts folder
mv ../../3-Combined${1}parts/*combined* ../../3-Combined${1}parts/

echo
echo "Process completed!"














