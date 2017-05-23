#! bin/bash

cd $1

for file in $(find . -name '*.txt'); do
	mv $file ${file%.txt}.creak
done