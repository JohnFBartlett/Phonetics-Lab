echo Resampling wav files in $1
cd $1
if ! [ -d Resampled ]
then
	mkdir Resampled
fi

pwd

for file in $(find . -name '*.wav'); do
	# only do this for the first part of each group
	echo "resampling " $file
	VAR=${file%.wav*}
	sox $file -r 16000 Resampled/${VAR}_rs.wav
done