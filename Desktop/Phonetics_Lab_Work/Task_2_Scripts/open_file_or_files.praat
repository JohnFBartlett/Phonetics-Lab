# Make a file list of all .wav files in current directory
list = Create Strings as file list: "Filelist", "*.wav"

form Test command line calls
    sentence wav_filename 
	sentence tg_filename
endform

# Open the files in Praat	
Read from file... 'wav_filename$'
Read from file... 'tg_filename$'


#### END OF SCRIPT ####