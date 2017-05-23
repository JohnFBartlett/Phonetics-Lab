# #! bin/bash

#find $1 -type f -name '*' -exec cat {} + >> MAIN_EXCEL

for f in $1/*; 
do 
	echo > n;
	cat "$f" n;
	echo; 
done > MAIN_EXCEL_VERT