#! bin/bash

echo "Formatting all files in $1 for import to Excel..."
cd $1

if [ ! -d For_Excel_Import ] 
then
	mkdir For_Excel_Import
fi

pwd

# format then paste files in order:
# .creak, .adjusted, .break, .f0

# do phrase
# do F01
FILE=$1'/COSPRO_01/F01/phrase'
for (( i=1; i < 600; i++ ))
do 
	# add 0's on front
	if [ "$i" -ge 1 -a "$i" -le 9 ]; then 
		num=00$i
	elif [ "$i" -ge 10 -a "$i" -le 99 ]; then 
		num=0$i
	else 
		num=$i
	fi
	if $(find . -name $FILE'/txt/COSPRO_01_F01phr'$num'.creak')
	then
		python format_for_paste.py $FILE'/txt/COSPRO_01_F01phr'$num'.creak' $1
		python format_for_paste.py $FILE'/adjusted/COSPRO_01_F01phr'$num'.adjusted' $1
		python format_for_paste.py $FILE'/break/COSPRO_01_F01phr'$num'.break' $1
		python format_for_paste.py $FILE'/f0/COSPRO_01_F01phr'$num'.f0' $1
		paste 'COSPRO_01_F01phr'$num'.creak_f' 'COSPRO_01_F01phr'$num'.adjusted_f' 'COSPRO_01_F01phr'$num'.break_f' 'COSPRO_01_F01phr'$num'.f0_f' > './For_Excel_Import/F01_'$num'_f'
		#mv F01.txt For_Excel_Import
	fi
done

# # do F02
FILE=$1'COSPRO_01/F02/phrase'
for (( i=1; i < 600; i++ ))
do 
	# add 0's on front
	if [ "$i" -ge 1 -a "$i" -le 9 ]; then 
		num=00$i
	elif [ "$i" -ge 10 -a "$i" -le 99 ]; then 
		num=0$i
	else 
		num=$i
	fi
	if $(find . -name $FILE'/txt/COSPRO_01_F02phr'$num'.creak')
	then
		python format_for_paste.py $FILE'/txt/COSPRO_01_F02phr'$num'.creak' $1
		python format_for_paste.py $FILE'/adjusted/COSPRO_01_F02phr'$num'.adjusted' $1
		python format_for_paste.py $FILE'/break/COSPRO_01_F02phr'$num'.break' $1
		python format_for_paste.py $FILE'/f0/COSPRO_01_F02phr'$num'.f0' $1
		paste 'COSPRO_01_F02phr'$num'.creak_f' 'COSPRO_01_F02phr'$num'.adjusted_f' 'COSPRO_01_F02phr'$num'.break_f' 'COSPRO_01_F02phr'$num'.f0_f' > './For_Excel_Import/F02_'$num'_f'
		#mv F01.txt For_Excel_Import
	fi
done

# # do F03
FILE=$1'COSPRO_01/F03/phrase'
for (( i=1; i < 600; i++ ))
do 
	# add 0's on front
	if [ "$i" -ge 1 -a "$i" -le 9 ]; then 
		num=00$i
	elif [ "$i" -ge 10 -a "$i" -le 99 ]; then 
		num=0$i
	else 
		num=$i
	fi
	if $(find . -name $FILE'/txt/COSPRO_01_F03phr'$num'.creak')
	then
		python format_for_paste.py $FILE'/txt/COSPRO_01_F03phr'$num'.creak' $1
		python format_for_paste.py $FILE'/adjusted/COSPRO_01_F03phr'$num'.adjusted' $1
		python format_for_paste.py $FILE'/break/COSPRO_01_F03phr'$num'.break' $1
		python format_for_paste.py $FILE'/f0/COSPRO_01_F03phr'$num'.f0' $1
		paste 'COSPRO_01_F03phr'$num'.creak_f' 'COSPRO_01_F03phr'$num'.adjusted_f' 'COSPRO_01_F03phr'$num'.break_f' 'COSPRO_01_F03phr'$num'.f0_f' > './For_Excel_Import/F03_'$num'_f'
		#mv F01.txt For_Excel_Import
	fi
done

# # do M01
FILE=$1'COSPRO_01/M01/phrase'
for (( i=1; i < 600; i++ ))
do 
	# add 0's on front
	if [ "$i" -ge 1 -a "$i" -le 9 ]; then 
		num=00$i
	elif [ "$i" -ge 10 -a "$i" -le 99 ]; then 
		num=0$i
	else 
		num=$i
	fi
	if $(find . -name $FILE'/txt/COSPRO_01_M01phr'$num'.creak')
	then
		python format_for_paste.py $FILE'/txt/COSPRO_01_M01phr'$num'.creak' $1
		python format_for_paste.py $FILE'/adjusted/COSPRO_01_M01phr'$num'.adjusted' $1
		python format_for_paste.py $FILE'/break/COSPRO_01_M01phr'$num'.break' $1
		python format_for_paste.py $FILE'/f0/COSPRO_01_M01phr'$num'.f0' $1
		paste 'COSPRO_01_M01phr'$num'.creak_f' 'COSPRO_01_M01phr'$num'.adjusted_f' 'COSPRO_01_M01phr'$num'.break_f' 'COSPRO_01_M01phr'$num'.f0_f' > './For_Excel_Import/M01_'$num'_f'
		#mv M01.txt For_Excel_Import
	fi
done

# # do M02
FILE=$1'COSPRO_01/M02/phrase'
for (( i=1; i < 600; i++ ))
do 
	# add 0's on front
	if [ "$i" -ge 1 -a "$i" -le 9 ]; then 
		num=00$i
	elif [ "$i" -ge 10 -a "$i" -le 99 ]; then 
		num=0$i
	else 
		num=$i
	fi
	if $(find . -name $FILE'/txt/COSPRO_01_M02phr'$num'.creak')
	then
		python format_for_paste.py $FILE'/txt/COSPRO_01_M02phr'$num'.creak' $1
		python format_for_paste.py $FILE'/adjusted/COSPRO_01_M02phr'$num'.adjusted' $1
		python format_for_paste.py $FILE'/break/COSPRO_01_M02phr'$num'.break' $1
		python format_for_paste.py $FILE'/f0/COSPRO_01_M02phr'$num'.f0' $1
		paste 'COSPRO_01_M02phr'$num'.creak_f' 'COSPRO_01_M02phr'$num'.adjusted_f' 'COSPRO_01_M02phr'$num'.break_f' 'COSPRO_01_M02phr'$num'.f0_f' > './For_Excel_Import/M02_'$num'_f'
		#mv M02.txt For_Excel_Import
	fi
done

# # do M03
FILE=$1'COSPRO_01/M03/phrase'
for (( i=1; i < 600; i++ ))
do 
	# add 0's on front
	if [ "$i" -ge 1 -a "$i" -le 9 ]; then 
		num=00$i
	elif [ "$i" -ge 10 -a "$i" -le 99 ]; then 
		num=0$i
	else 
		num=$i
	fi
	if $(find . -name $FILE'/txt/COSPRO_01_M03phr'$num'.creak')
	then
		python format_for_paste.py $FILE'/txt/COSPRO_01_M03phr'$num'.creak' $1
		python format_for_paste.py $FILE'/adjusted/COSPRO_01_M03phr'$num'.adjusted' $1
		python format_for_paste.py $FILE'/break/COSPRO_01_M03phr'$num'.break' $1
		python format_for_paste.py $FILE'/f0/COSPRO_01_M03phr'$num'.f0' $1
		paste 'COSPRO_01_M03phr'$num'.creak_f' 'COSPRO_01_M03phr'$num'.adjusted_f' 'COSPRO_01_M03phr'$num'.break_f' 'COSPRO_01_M03phr'$num'.f0_f' > './For_Excel_Import/M03_'$num'_f'
		#mv M03.txt For_Excel_Import
	fi
done

# cd ~/Desktop/Active/For_Excel_Import
# # touch finished.txt
# for (( i=1; i < 600; i++ ))
# do
# 	#add 0's on front
# 	if [ "$i" -ge 1 -a "$i" -le 9 ]; then 
# 		num=00$i
# 	elif [ "$i" -ge 10 -a "$i" -le 99 ]; then 
# 		num=0$i
# 	else 
# 		num=$i
# 	fi
# 	paste -d',' 'F01_'$num'_f_fixed_spaced' 'F02_'$num'_f_fixed_spaced' 'F03_'$num'_f_fixed_spaced' 'M01_'$num'_f_fixed_spaced' 'M02_'$num'_f_fixed_spaced' 'M03_'$num'_f_fixed_spaced' > './Combined_speakers/EXCEL_DATA_'$num
# done

