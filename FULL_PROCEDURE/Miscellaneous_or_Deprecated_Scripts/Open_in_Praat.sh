#!/bin/bash

# see how many arguments there are
if [ "$#" -e 2 ]; then
    if [[ "$2" = "COSPRO" ]]; then
	    OTHER=$1


# otherwise take user through directory
else
	ALLSP=0
	echo
	echo -n "Choose speaker (F01, F02, F03, M01, M02, M03, all): "
	read speaker

	case $speaker in

    [Ff]01 | [Ff]1)
        echo "Speaker F01"
        echo
        speaker=F01
        ;;
    [Ff]02 | [Ff]2)
        echo "Speaker F02"
        echo
        speaker=F02
        ;;
    [Ff]03 | [Ff]3)
        echo "Speaker F03"
        echo
        speaker=F03
        ;;
    [Mm]01 | [Mm]1)
        echo "Speaker M01"
        echo
        speaker=M01
        ;;
    [Mm]02 | [Mm]2)
        echo "Speaker M02"
        echo
        speaker=M02
        ;;
    [Mm]03 | [Mm]3)
        echo "Speaker M03"
        echo
        speaker=M03
        ;;
    [Aa][Ll][Ll])
        # confirm that the user wants to open for all speakers
		# echo -n "Are you sure you want to open all speakers? "
  #       read ANS
        # if ! [ $ANS = [Yy][Ee][Ss] ]; then
        # 	exit 0;
        # fi
        echo "Choosing file for all speakers."
        ALLSP=1
        ;;
    *)
        echo "$speaker is not a valid speaker."
        echo
        exit 1
        ;;
	esac

	# now ask what type of file
	echo -n "Word or Phrase?: "
	read TYPE

	case $TYPE in

		# word or w selected (case insensitive)
		[Ww][Oo][Rr][Dd] | [Ww])
			echo "Word"
			echo
			TYPE=word

			echo -n "Choose file number: "
			read number
			if [[ "$number" =~ ^[0-9]+$ ]]; then
				# check if numbers are within range and format them if they are
				if [ "$number" -le 0 ]; then 
					echo "Word $number does not exist."
					exit;
				elif [ "$number" -ge 1 -a "$number" -le 9 ]; then 
					number=000$number
					echo $number;
				elif [ "$number" -ge 10 -a "$number" -le 99 ]; then 
					number=00$number
					echo $number;
				elif [ "$number" -ge 100 -a "$number" -le 999 ]; then 
					number=0$number
					echo $number;
				elif [ "$number" -ge 1455 ]; then 
					echo "Word $number does not exist."
					exit;
				fi
				
				# get location of data directory
				COS=$(find . -type d -name "COSPRO_01")
				if ! [ $COS ]; then
					echo "Can't find COSPRO_01 directory!"
				fi

				# check if file is being opened for all speakers
				if [ $ALLSP -eq 1 ]; then
					W1=$COS"/F01/word/wav/COSPRO_01_F01w"$number".wav"
					W2=$COS"/F02/word/wav/COSPRO_01_F02w"$number".wav"
					W3=$COS"/F03/word/wav/COSPRO_01_F03w"$number".wav"
					W4=$COS"/M01/word/wav/COSPRO_01_M01w"$number".wav"
					W5=$COS"/M02/word/wav/COSPRO_01_M02w"$number".wav"
					W6=$COS"/M03/word/wav/COSPRO_01_M03w"$number".wav"
					T1=$COS"/F01/word/TextGrid/COSPRO_01_F01w"$number".TextGrid"
					T2=$COS"/F02/word/TextGrid/COSPRO_01_F02w"$number".TextGrid"
					T3=$COS"/F03/word/TextGrid/COSPRO_01_F03w"$number".TextGrid"
					T4=$COS"/M01/word/TextGrid/COSPRO_01_M01w"$number".TextGrid"
					T5=$COS"/M02/word/TextGrid/COSPRO_01_M02w"$number".TextGrid"
					T6=$COS"/M03/word/TextGrid/COSPRO_01_M03w"$number".TextGrid"
					/Applications/Praat.app/Contents/MacOS/Praat --open $W1 $T1 $W2 $T2 $W3 $T3 $W4 $T4 $W5 $T5 $W6 $T6;
				# otherwise open the specified file
				else
					WAV=$COS"/"$speaker"/word/wav/COSPRO_01_"$speaker"w"$number".wav"
					echo $WAV
					TG=$COS"/"$speaker"/word/TextGrid/COSPRO_01_"$speaker"w"$number".TextGrid"
					echo $TG
					/Applications/Praat.app/Contents/MacOS/Praat --open $WAV $TG;
				fi
				
			else 
				# opening "all" is not yet supported
				echo "$number is not an integer."
				echo; 
			fi

			;;

		# phrase or p selected (case insensitive)
		[Pp][Hh][Rr][Aa][Ss][Ee] | [Pp])
			echo "Phrase"
			echo
			TYPE=phrase

			echo -n "Choose file number: "
			read number
			if [[ "$number" =~ ^[0-9]+$ ]]; then
				# check if numbers are within range and format them if they are
				if [ "$number" -le 0 ]; then 
					echo "Phrase $number does not exist."
					exit;
				elif [ "$number" -ge 1 -a "$number" -le 9 ]; then 
					number=00$number
					echo $number;
				elif [ "$number" -ge 10 -a "$number" -le 99 ]; then 
					number=0$number
					echo $number;
				elif [ "$number" -ge 599 ]; then 
					echo "Phrase $number does not exist."
					exit;
				fi

				echo "Opening phrase $number for $speaker..."; 

				# get location of data directory
				COS=$(find . -type d -name "COSPRO_01")
				if ! [ $COS ]; then
					echo "Can't find COSPRO_01 directory!"
				fi

				# check if file is being opened for all speakers
				if [ $ALLSP -eq 1 ]; then
					W1=$COS"/F01/phrase/wav/COSPRO_01_F01phr"$number".wav"
					W2=$COS"/F02/phrase/wav/COSPRO_01_F02phr"$number".wav"
					W3=$COS"/F03/phrase/wav/COSPRO_01_F03phr"$number".wav"
					W4=$COS"/M01/phrase/wav/COSPRO_01_M01phr"$number".wav"
					W5=$COS"/M02/phrase/wav/COSPRO_01_M02phr"$number".wav"
					W6=$COS"/M03/phrase/wav/COSPRO_01_M03phr"$number".wav"
					T1=$COS"/F01/phrase/TextGrid/COSPRO_01_F01phr"$number".TextGrid"
					T2=$COS"/F02/phrase/TextGrid/COSPRO_01_F02phr"$number".TextGrid"
					T3=$COS"/F03/phrase/TextGrid/COSPRO_01_F03phr"$number".TextGrid"
					T4=$COS"/M01/phrase/TextGrid/COSPRO_01_M01phr"$number".TextGrid"
					T5=$COS"/M02/phrase/TextGrid/COSPRO_01_M02phr"$number".TextGrid"
					T6=$COS"/M03/phrase/TextGrid/COSPRO_01_M03phr"$number".TextGrid"
					/Applications/Praat.app/Contents/MacOS/Praat --open $W1 $T1 $W2 $T2 $W3 $T3 $W4 $T4 $W5 $T5 $W6 $T6;
				else
					WAV=$COS"/"$speaker"/phrase/wav/COSPRO_01_"$speaker"phr"$number".wav"
					echo $WAV
					TG=$COS"/"$speaker"/phrase/TextGrid/COSPRO_01_"$speaker"phr"$number".TextGrid"
					echo $TG
					/Applications/Praat.app/Contents/MacOS/Praat --open $WAV $TG;
				fi
			else 
				echo "$number is not an integer."
				echo; 
			fi
			;;
		[Aa][Ll][Ll] | [Bb][Oo][Tt][Hh])
        	echo "You picked both."
        	echo

        	echo -n "Choose file number: "
			read number
			if [[ "$number" =~ ^[0-9]+$ ]]; then
				# check if numbers are within range and format them if they are
				if [ "$number" -le 0 ]; then 
					echo "Phrase $number does not exist."
					exit;
				elif [ "$number" -ge 1 -a "$number" -le 9 ]; then 
					number=00$number
					echo $number
					echo "Opening phrase and word $number for $speaker...";
				elif [ "$number" -ge 10 -a "$number" -le 99 ]; then 
					number=0$number
					echo $number
					echo "Opening phrase and word $number for $speaker...";
				elif [ "$number" -ge 599 ]; then 
					echo "Phrase $number does not exist."
					if [ "$number" -ge 1455 ]; then 
						echo "Word $number does not exist. Exiting."
						exit;
					else
						echo "Opening only word $number."
					fi
				fi

				# get location of data directory
				COS=$(find . -type d -name "COSPRO_01")
				if ! [ $COS ]; then
					echo "Can't find COSPRO_01 directory!"
				fi

				# check if file is being opened for all speakers
				if [ $ALLSP -eq 1 ]; then
					PW1=$COS"/F01/phrase/wav/COSPRO_01_F01phr"$number".wav"
					PW2=$COS"/F02/phrase/wav/COSPRO_01_F02phr"$number".wav"
					W3=$COS"/F03/phrase/wav/COSPRO_01_F03phr"$number".wav"
					PW4=$COS"/M01/phrase/wav/COSPRO_01_M01phr"$number".wav"
					PW5=$COS"/M02/phrase/wav/COSPRO_01_M02phr"$number".wav"
					PW6=$COS"/M03/phrase/wav/COSPRO_01_M03phr"$number".wav"
					PT1=$COS"/F01/phrase/TextGrid/COSPRO_01_F01phr"$number".TextGrid"
					PT2=$COS"/F02/phrase/TextGrid/COSPRO_01_F02phr"$number".TextGrid"
					PT3=$COS"/F03/phrase/TextGrid/COSPRO_01_F03phr"$number".TextGrid"
					PT4=$COS"/M01/phrase/TextGrid/COSPRO_01_M01phr"$number".TextGrid"
					PT5=$COS"/M02/phrase/TextGrid/COSPRO_01_M02phr"$number".TextGrid"
					PT6=$COS"/M03/phrase/TextGrid/COSPRO_01_M03phr"$number".TextGrid"
					WW1=$COS"/F01/word/wav/COSPRO_01_F01w"$number".wav"
					WW2=$COS"/F02/word/wav/COSPRO_01_F02w"$number".wav"
					WW3=$COS"/F03/word/wav/COSPRO_01_F03w"$number".wav"
					WW4=$COS"/M01/word/wav/COSPRO_01_M01w"$number".wav"
					WW5=$COS"/M02/word/wav/COSPRO_01_M02w"$number".wav"
					WW6=$COS"/M03/word/wav/COSPRO_01_M03w"$number".wav"
					WT1=$COS"/F01/word/TextGrid/COSPRO_01_F01w"$number".TextGrid"
					WT2=$COS"/F02/word/TextGrid/COSPRO_01_F02w"$number".TextGrid"
					WT3=$COS"/F03/word/TextGrid/COSPRO_01_F03w"$number".TextGrid"
					WT4=$COS"/M01/word/TextGrid/COSPRO_01_M01w"$number".TextGrid"
					WT5=$COS"/M02/word/TextGrid/COSPRO_01_M02w"$number".TextGrid"
					WT6=$COS"/M03/word/TextGrid/COSPRO_01_M03w"$number".TextGrid"
					/Applications/Praat.app/Contents/MacOS/Praat --open $PW1 $PT1 $PW2 $PT2 $PW3 $PT3 $PW4 $PT4 $PW5 $PT5 $PW6 $PT6 $WW1 $WT1 $WW2 $WT2 $WW3 $WT3 $WW4 $WT4 $WW5 $WT5 $WW6 $WT6;
				else
					PWAV=$COS"/"$speaker"/phrase/wav/COSPRO_01_"$speaker"phr"$number".wav"
					echo $PWAV
					PTG=$COS"/"$speaker"/phrase/TextGrid/COSPRO_01_"$speaker"phr"$number".TextGrid"
					echo $PTG
					WWAV=$COS"/"$speaker"/word/wav/COSPRO_01_"$speaker"w"$number".wav"
					echo $WWAV
					WTG=$COS"/"$speaker"/word/TextGrid/COSPRO_01_"$speaker"w"$number".TextGrid"
					echo $WTG
					/Applications/Praat.app/Contents/MacOS/Praat --open $PWAV $PTG $WWAV $WTG;
				fi
			else 
				echo "$number is not an integer."
				echo; 
			fi
       	 ;;
		*)
        	echo "$TYPE is not a valid option."
        	;;
	esac;
fi
