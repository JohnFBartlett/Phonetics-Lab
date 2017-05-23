#!/usr/bin/python

import sys, re
from numpy import empty

def make_txtgrid_format(f):
	print "making textGrid from .adjusted or .phn"
	tempTime = ''
	currState = ''
	numTime = -1
	intervals = []
	intervalUnit = ['']*3

	# initialize txtGrid file
	# remove syl extension
	filetype = ''
	if "adjusted" in f:
		# remove adjusted_fixed
		fileTitle = f[:-14] + 'TextGrid'
		filetype = "a"
	elif "phn" in f:
		# remove phn_fixed
		fileTitle = f[:-9] + 'TextGrid'
		filetype = "p"
	else:
		raise ValueError("Wrong input file type.")
	tg = open(fileTitle, 'w')
	tg.write('File type = "ooTextFile"\n')
	tg.write('Object class = "TextGrid"\n\n')
	tg.write('xmin = 0\n')

	# get intervals for creak tier
	with open(f) as file:
		for line in file:
			if 'Milliseconds' in line:
				continue
			if 'END' in line:
				continue
			else:
				# print "\n\nCurrent line is " + line
				# lineInfo = line.split(' |\t')
				try:
					lineInfo = re.split(' |\t', line)
					# print lineInfo
					# adjust numbers
					# print "before " + lineInfo[0] + " to " + lineInfo[1]
					lineInfo[0] = str(float(lineInfo[0])/1000)
					lineInfo[1] = str(float(lineInfo[1])/1000)
					# print "after " + lineInfo[0] + " to " + lineInfo[1]
				except ValueError:
					print line
					raise ValueError("Formatted incorrectly")
				intervals.append(lineInfo)

	# print rest of txtGrid file
	tg.write('xmax = ' + str(intervals[-1][1]) + '\n')
	tg.write('tiers? <exists>\n')
	tg.write('size = 1\n')
	tg.write('item []:\n')
	tg.write('    ' + 'item [1]:\n')
	tg.write('        ' + 'class = "IntervalTier"\n')
	tg.write('        ' + 'name = "Syllables"\n')
	tg.write('        ' + 'xmin = 0\n')
	tg.write('        ' + 'xmax = ' + str(intervals[-1][-2]) + '\n')
	tg.write('        ' + 'intervals: size = ' + str(len(intervals)) + '\n')
	for i in xrange(0, len(intervals), 1):
		unit = intervals[i]
		unit[2] = re.sub(r'(.*)\n', r'\1', unit[2])
		tg.write('        ' + 'intervals [' + str(i+1) + ']:\n')
		tg.write('            ' + 'xmin = ' + unit[0] + '\n')
		tg.write('            ' + 'xmax = ' + unit[1] + '\n')
		tg.write('            ' + 'text = ' + '"' + str(unit[2]) + '"' + '\n')
		unit = []

	tg.close()
	#print "number of intervals: " + str(len(intervals))
	#print intervals

make_txtgrid_format(sys.argv[1])