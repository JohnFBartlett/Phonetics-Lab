# Make a file list of all .wav files in current directory
list = Create Strings as file list: "Filelist", "*.wav"

# iterate through each file
n = Get number of strings
pause 'n' files were identified.  Continue?

for i to n
    selectObject: list
    filename$ = Get string: i

	# Open the long sound file
	Open long sound file... 'filename$'
	Rename... lsound
    
    # Get the duration of the file
	startTime = Get starting time
	finishTime = Get finishing time
	
	# Set initial interval times
	startInterval = startTime
	endInterval = startTime + 5
	
	intLabel = 0
	while finishTime > endInterval
		# convert to string, add 0 if necessary
		if intLabel < 10
			num$ = "0" + string$ (intLabel)
		else
			num$ = string$ (intLabel)
		endif

		# make the title of the piece
		outTitle$ = filename$ - ".wav" + "part" + num$ + ".wav"
		
		# now get interval and save it
		select LongSound lsound
		Extract part... startInterval endInterval yes
		Rename... part_'num$'
		Write to WAV file... ./pieces/'outTitle$'
		
		#remove sound piece
		select Sound part_'num$'
		Remove
		
		# increment interval start/end and intLabel
		startInterval = startInterval + 5
		endInterval = endInterval + 5
		intLabel = intLabel + 1
	endwhile
	
	# put last bit of the sound into another file
	# convert to string, add 0 if necessary
	if intLabel < 10
		num$ = "0" + string$ (intLabel)
	else
		num$ = string$ (intLabel)
	endif

	# make the title of the piece
	outTitle$ = filename$ - ".wav" + "part" + num$ + ".wav"
		
	# now get interval and save it
	select LongSound lsound
	Extract part... startInterval endInterval yes
	Rename... part_'num$'
	Write to WAV file... ./pieces/'outTitle$'

	#remove sound piece
	select Sound part_'num$'
	Remove
	
    # remove sound object
	select LongSound lsound
    Remove
endfor
removeObject: list

pause Finished segmenting all files.

#### END OF SCRIPT ####