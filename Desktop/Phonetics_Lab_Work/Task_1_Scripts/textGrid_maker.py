#!/usr/bin/python

import sys
from numpy import empty

def make_txtgrid_format(f):
	tempTime = ''
	currState = ''
	numTime = -1
	intervals = []
	intervalUnit = ['']*3

	# initialize txtGrid file
	fileTitle = f[:-3] + 'TextGrid'
	tg = open(fileTitle, 'w')
	tg.write('File type = "ooTextFile"\n')
	tg.write('Object class = "TextGrid"\n\n')
	tg.write('xmin = 0\n')

	# get intervals for creak tier
	with open(f) as file:
		for line in file:
			if line == 'Var1_1,Var1_2\n':
				continue
			else:
				# print "\n\nCurrent line is " + line
				[tempTime, tempState] = line.split(',')

				if intervalUnit[0] == '':
					# print "New interval"
					numTime = float(tempTime)
					numTime -= 0.01
					tempTime = str(numTime)
					intervalUnit[0] = tempTime
					intervalUnit[2] = int(tempState)

				elif intervalUnit[2] != int(tempState):
					#print "end of interval"
					#print tempState
					#print tempTime
					intervalUnit[1] = tempTime
					# put iu in interval set
					intervals.append(intervalUnit)
					#print intervals
					# clear iu
					intervalUnit = ['', '', -1]
				else: 
					# print "same"
					continue
	# finish last interval
	intervalUnit[1] = tempTime
	intervals.append(intervalUnit)

	# print rest of txtGrid file
	tg.write('xmax = ' + str(intervals[-1][-2]) + '\n')
	tg.write('tiers? <exists>\n')
	tg.write('size = 1\n')
	tg.write('item []:\n')
	tg.write('    ' + 'item [1]:\n')
	tg.write('        ' + 'class = "IntervalTier"\n')
	tg.write('        ' + 'name = "Creaky_Classification"\n')
	tg.write('        ' + 'xmin = 0\n')
	tg.write('        ' + 'xmax = ' + str(intervals[-1][-2]) + '\n')
	tg.write('        ' + 'intervals: size = ' + str(len(intervals)) + '\n')
	for i in xrange(0, len(intervals), 1):
		unit = intervals[i]
		tg.write('        ' + 'intervals [' + str(i+1) + ']:\n')
		tg.write('            ' + 'xmin = ' + unit[0] + '\n')
		tg.write('            ' + 'xmax = ' + unit[1] + '\n')
		tg.write('            ' + 'text = ' + '"' + str(unit[2]) + '"' + '\n')
		unit = []

	tg.close()
	#print "number of intervals: " + str(len(intervals))
	#print intervals

make_txtgrid_format(sys.argv[1])