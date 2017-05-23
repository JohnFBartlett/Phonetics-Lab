# Make a file list of all .wav files in current directory
list = Create Strings as file list: "Filelist", "*.wav"

# iterate through each file
n = Get number of strings
pause 'n' files were identified.  Continue?

for i to n
    selectObject: list
    filename$ = Get string: i

	# Open the long sound file
	Read from file... 'filename$'

	# Extract channel 1
	Extract one channel... 1

	# Make var for name to be selected
	newSound$ = filename$ - ".wav" + "_ch1"
	newTitle$ = newSound$ + ".wav"
	oldSound$ = filename$ - ".wav"

	# Select and write created file
	select Sound 'newSound$'
	Write to WAV file... ./extracted/'newTitle$'

	# remove new sound
	select Sound 'newSound$'
	Remove

	# remove old sound
	select Sound 'oldSound$'
	Remove
endfor
removeObject: list

pause Finished segmenting all files.

#### END OF SCRIPT ####