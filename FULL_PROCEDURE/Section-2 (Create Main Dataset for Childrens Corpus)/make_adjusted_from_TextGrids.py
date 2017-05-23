#!/usr/bin/python

# Uses labeled syllable TextGrids for the Children's corpus
# to create .adjusted files for the Children's corpus
# example python make_adjusted_from_TextGrids.py $file

import sys, re
from os.path import isfile

def create_adjusted(textgrid):
	if isfile(textgrid):
		if ".TextGrid" in textgrid:
			print("creating from file: " + textgrid)

			# create out file
			name = re.sub(r'(.*)\.TextGrid', r'\1', textgrid)
			outName = name + '.adjusted'
			out = open(outName, 'w')

			# Add heading
			out.write("MillisecondsPerFrame: 1.0\nEND OF HEADER\n")

			with open(textgrid, 'r') as tg:
				rightItem = False
				rightSection = False
				for line in tg:
					# skip until you get to item 4 interval 1
					if not rightSection:
						if not rightItem:
							if "item [4]:" in line:
								rightItem = True
								continue
							else:
								continue
						else:
							if "intervals [1]:" in line:
								rightSection = True
								continue
							else:
								continue

					# get min, convert to milliseconds and round down
					if "xmin" in line:
						pieces = line.split(' ')
						xmin = pieces[-2]

						# convert number
						num = float(xmin)
						num = num*1000
						intNum = int(num)
						xmin = str(intNum)

						# write min + space
						out.write(xmin + ' ')

					# get max, convert to milliseconds and round down
					if "xmax" in line:
						pieces = line.split(' ')
						xmax = pieces[-2]

						# convert number
						num = float(xmax)
						num = num*1000
						intNum = int(num)
						xmax = str(intNum)
						out.write(xmax + ' ')

					# get segment
					if "text = " in line:
						segment = re.sub(r'text = \"(.*)\"', r'\1', line)
						# write segment plus newline
						segment = segment.strip('\t\n ')
						out.write(segment + '\n')
			out.close()
		else:
			print("Inputted file ")
	else:
		print("Invalid file given!")
		while True:
			continue

create_adjusted(sys.argv[1])