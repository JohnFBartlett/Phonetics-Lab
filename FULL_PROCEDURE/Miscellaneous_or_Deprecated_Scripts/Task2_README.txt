1. ran cut_into_intervals.praat on all long .wav files to make them no longer than 5 seconds so Voicesauce could handle them easily

2. started running Voicesauce on the segmented .wav files to get .mat files

3. ran Count_tones.py and then Add_tone_counts.py (using apply_python_script.sh) to get tone counts for all files (T0(or T5), T1, T2, T3, T4, T2T3, T3T3), and then combine them to get totals for each speaker

4. started running Voicesauce to convert .mat files to .txt files (this created one enormous text file that combined all the converted .mat files inputted)

5. ran convert_to_segment_intervals.py on the text files so each row was the average of all lines of data that occurred within a segment interval (had to make a new version of cut_into_intervals.praat because of a small formatting error which led to two versions of convert_to_segment_intervals.py — in future iterations only the newer one would be necessary). The outputs of this are files with the extension .measures

6. ran format_for_Task2_sheet.py: this is the main script which found and printed speech style and speaker information based on filenames, and used the combinations of multiple file types to get breaks that lined up with each segment, whether each segment had a vowel, and other info to paste along with the measurements from VoiceSauce (after they’d been converted to segment intervals). Files created by format_for_Task2_sheet.py (.t2 extension) can be imported directly into Excel 

7. pasted .t2 files together to get large sections of data that could be imported to Excel all at once (called COMBINED.t2)