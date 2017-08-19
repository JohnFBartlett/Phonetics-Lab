#! bin/bash

# Sample execution:
# plab -b Section-1_making_COSPRO_Dataset/master_script.sh {CORPUS NAME} {part number}
echo "----------------------------------------------------------------"
echo "Beginning Phonetics Lab data analysis procedure on corpus $1"

cd ~/Documents/Phonetics_Lab_Summer_2017/Phonetics-Lab/COSPRO_DATA_BIN/data_analysis/0-Base_Files/

cd $1 || echo "$1 does not exist in directory 0-Base_Files/"

# Check if scripts section is specified
if [ $# -eq 2 ]
then
    echo "Part number found"
    PART=$2
else
    PART=1
fi

if [ "$PART" -eq 1 ]
then
    echo -n "Starting with Phase 1: Initial Steps. Begin?(y/n) "
    read yn
    if [[ "$yn" =~ ^(n|N|no|No) ]]; then
        exit 0
    fi

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
fi

if [ "$PART" -lt 3 ]
then
    echo -n "VoiceSauce, Creak and Reaper Analysis. Begin?(y/n) "
    read yn
    if [[ "$yn" =~ ^(n|N|no|No) ]]; then
        exit 0
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
        fi
        echo -n "Continue?(y/n)"
        read yn
        if [[ "$yn" =~ ^(n|N|no|No) ]]; then
            quit 0
        fi
        echo "Continuing while Matlab runs in background..."
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

    # Ask about Phase 3: Reaper Analysis
    echo
    echo -n "Has Reaper analysis been run, or is it being run, on desired files?(y/n)"
    read yn
    if [[ "$yn" =~ ^(n|N|no|No) ]]; then
        plab -b Section-1_making_COSPRO_Dataset/Phase-3_Reaper_Analysis/apply_reaper .
        find ./Output/ -name *creak -exec mv {} ../../1-Raw_Reaper/$1
    fi

    echo "Completed Analysis section."
fi


if [ "$PART" -lt 4 ]
then
    echo
    echo -n "Phase 5: File Alignment. Begin?(y/n) "
    read yn
    if [[ "$yn" =~ ^(n|N|no|No) ]]; then
        exit 0
    fi
    echo
    echo "Checking for adjusted files..."
    # Check reaper
    if [[ -n "$(ls ../../2-Formatted_Segments/$1)" ]]; then
        echo "Found adjusted/phn files"
    else
        echo "No files found in ../../2-Formatted_Adjusted! Cannot format other files without .adjusted or .phn files"
        pwd
    fi

    # Check reaper
    echo -n "Have reaper files been formatted?(y/n) "
    read yn
    if [[ "$yn" =~ ^(n|N|no|No) ]]; then
        echo "Checking for reaper files..."
        if [[ -n "$(ls ../../1-Raw_Reaper_Results/$1)" ]]; then
            echo "Found files in Raw Reaper folder"
            CURRTIME=date +"%Y-%m-%d_%T"
            LOGNAME="reaper_formatting_$CURRTIME.log"
            python ~/Documents/Phonetics_Lab_Summer_2017/Phonetics-Lab/FULL_PROCEDURE/Section-1_making_COSPRO_Dataset/Phase-5_Align_Files/convert_to_15_intervalsV2.py reaper $1 10 $LOGNAME
        else
            echo "No files found in ../../1-Raw_Reaper_Results!"
            pwd
        fi
    fi

    # Check creak
    echo -n "Have creak files been formatted?(y/n) "
    read yn
    if [[ "$yn" =~ ^(n|N|no|No) ]]; then
        echo "Checking for creak files..."
        if [[ -n "$(ls ../../1-Raw_Creaks/$1)" ]]; then
            echo "Found files in Raw Creak folder"
            CURRTIME=date +"%Y-%m-%d_%T"
            LOGNAME="creak_formatting_$CURRTIME.log"
            python ~/Documents/Phonetics_Lab_Summer_2017/Phonetics-Lab/FULL_PROCEDURE/Section-1_making_COSPRO_Dataset/Phase-5_Align_Files/convert_to_15_intervalsV2.py creak $1 10 $LOGNAME
        else
            echo "No files found in ../../1-Raw_Creaks!"
            pwd
        fi
    fi

    # Check Measures
    echo -n "Have VoiceSauce files been split into segments?(y/n)"
    read yn
    if [[ "$yn" =~ ^(n|N|no|No) ]]; then
        if [[ -n "$(ls ../../1-Raw_Measures/$1)" ]]; then
            echo "Found files in Raw Measures folder"
            for file in $(find ../../1-Raw_Measures/$1 -name *combined*txt); do
                echo "Opening file $file"
                CURRTIME=date +"%Y-%m-%d_%T"
                LOGNAME="../../logs/measures_formatting_$CURRTIME"
                python ~/Documents/Phonetics_Lab_Summer_2017/Phonetics-Lab/FULL_PROCEDURE/Section-1_making_COSPRO_Dataset/Phase-5_Align_Files/split_measures.py ../../1-Raw_Measures/$1$file ../../2-Formatted_Measures/$1 $LOGNAME
            done

        else
            echo "No files found in ../../1-Raw_Measures!"
            pwd
        fi
    fi

    echo
    echo "Files formatted."
fi

# Do Phase 6: Create combined Dataset
echo -n "Phase 6: Creating combined dataset. Begin?(y/n) "
read yn
if [[ "$yn" =~ ^(n|N|no|No) ]]; then
    exit 0
fi

echo -n "Format files?(y/n) "
read yn
if [[ "$yn" =~ ^(y|Y|yes|Yes) ]]; then
    # Run task2_formatting
    CURRTIME=date +"%Y-%m-%d_%T"
    LOGNAME="../../logs/creating_dataset_$CURRTIME"
    bash ~/Documents/Phonetics_Lab_Summer_2017/Phonetics-Lab/FULL_PROCEDURE/Section-1_making_COSPRO_Dataset/Phase-6_Create_Combined_Dataset/apply_task2_formatting.sh $1 $LOGNAME

fi

cd ../../3-Combined/$1
pwd
echo -n "Combine files?(y/n) "
read yn
if [[ "$yn" =~ ^(n|N|no|No) ]]; then
    exit 0
fi
echo "Now combining files"
# Go into parts and combine tables
corpus=${1%/}
CURRTIME=date +"%Y-%m-%d_%T"
LOGNAME="../../logs/combining_files_$CURRTIME"
python ~/Documents/Phonetics_Lab_Summer_2017/Phonetics-Lab/FULL_PROCEDURE/Section-1_making_COSPRO_Dataset/Phase-6_Create_Combined_Dataset/combine_tables.py parts/ $corpus_combined.txt $LOGNAME

# Move combined file out of the parts folder
mv parts/$corpus_combined.txt .

echo
echo "Process completed!"









