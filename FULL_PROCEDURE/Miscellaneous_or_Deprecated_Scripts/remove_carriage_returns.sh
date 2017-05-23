#! bin/bash
 for file in $1*.txt
 do 
 	echo $file
 	tr -d '\r' < $file > $file'_fixed'
 done