#!/usr/bin/python

import sys, re
from numpy import empty

def label_txtgrid(f, database):
	# set initial progress values
	checkItem = False
	checkClass = False
	checkName = False
	written = 0

	# determine sentence type used in file
	sentenceNum = int(re.sub(r'.*_t(\d{3})_.*', r'\1', f))
	print str(sentenceNum)

	# match num with correct words for the file
	data = open(database, 'r')
	for _ in xrange(sentenceNum+1):
		line = next(data)
	matchLine = line.split(',')
	data.close()
	try:
		# print matchLine
		[word1_2, word3, word4] = [matchLine[6], matchLine[9], matchLine[13]]
		print "[" + word1_2 + "," + word3 + "," +  word4 + "]"
		# split word 1_2
		[word1, word2] = word1_2.split('_')
	except:
		print("word1_2 is " + word1_2)
		raise Exception("Can't split 1_2 into two words.")

	# initialize new txtGrid file
	# remove creak_aligned extension
	fileTitle = f[:-9] + '-labeled.TextGrid'
	tg = open(fileTitle, 'w')

	# get intervals for creak tier
	with open(f) as file:
		for line in file:
			# make sure file is formatted correctly
			# and get to the right spot in the file
			if not checkName:
				if not checkClass:
					if not checkItem:
						if 'item [4]:' not in line:
							tg.write(line)
							continue
						else:
							checkItem = True
							tg.write(line)
							continue
					elif 'class = "IntervalTier"' in line:
						checkClass = True
						tg.write(line)
						continue
					# if class line not found immediately after, print error message
					else:
						print "line is " + line
						raise ValueError("Correct class not found!")
				elif 'name = "Syllables"' in line:
					checkName = True
					tg.write(line)
					continue
				# if class line not found immediately after, print error message
				else:
					print "line is " + line
					raise ValueError("Correct name not found!")

			if 'text = ""' in line:
				if written == 0:
					tg.write('            text = "' + word1 + '"\n')
					written = 1
				elif written == 1:
					tg.write('            text = "' + word2 + '"\n')
					written = 2
				elif written == 2:
					tg.write('            text = "' + word3 + '"\n')
					written = 3
				elif written == 3:
					tg.write('            text = "' + word4 + '"\n')
					written = 4
				else:
					raise ValueError("All words have been written already!")
			else:
				tg.write(line)


	tg.close()
	#print "number of intervals: " + str(len(intervals))
	#print intervals

label_txtgrid(sys.argv[1], sys.argv[2])