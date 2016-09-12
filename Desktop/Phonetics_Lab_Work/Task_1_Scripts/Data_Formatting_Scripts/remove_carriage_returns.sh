#! bin/bash
 for file in $1*
 do 
 	tr -d '\r' < $file > $file'_fixed'
 done