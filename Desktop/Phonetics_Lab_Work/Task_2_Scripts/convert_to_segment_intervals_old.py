#!/usr/bin/python

import sys
import re
from os import listdir
from os.path import isfile
import Queue

# initialize universal part storage variable
storage = Queue.Queue()

def format_files(adjusted, otherFile, outpath):
    
    if ".break" in otherFile:
        print "break file"
    if ".txt" in otherFile:
        # open .adjusted, .break, and .measurements files for this title
        with open(otherFile, 'r') as m:
            # store header line, remove first two header fields
            header = next(m)
            header = header[3:]

            # create variables for averaging
            lines = []
            avgline = []

            # check if adjusted is a directory
            if isfile(adjusted):
                print("Please enter a directory of adjusted files.")

            # if so, get all files in directory
            files = listdir(adjusted)

            print(files)
            for f in files:
                # remove adjusted extension
                name = f[:-9]
                # print("name is " + name)
                # .measures is the extension of voicesauce measurements formatted to segment intervals
                fileTitle = outpath + name + '.measures'
                out = open(fileTitle, 'w')

                #write header
                out.write(header)

                with open(f, 'r') as a:
                    try:
                        next(a)
                        next(a)
                    except IOError:
                        print("File has fewer than two lines of content.\n")
                        print("It is probably either the wrong type of file or was created incorrectly.\n")
                    # look at one line at a time
                    first = 1
                    for line in a:
                        try:
                            # print "A line is " + line
                            [currStart, currEnd, currSegment] = line.split(' ')
                        except IOError:
                            print("File cannot be split into three parts.\n")
                            print("It is probably either the wrong type of file or was created incorrectly.\n")

                        if first:
                            # get lines between start and end
                            mLine = next(m).split('\t')
                            # remove newline character for calculations
                            mLine = mLine[:-1]

                            # get timestamp of measurements line (adjusted for parts 0-6)
                            # each part is up to 5000 milliseconds, so while part 1 says it starts
                            # at 1 millisecond, it really starts at 5001 milliseconds
                            addedTime = float(re.sub(r'.*part(\d{1,2}).mat', r'\1', mLine[0])) * 5000
                            mLine[4] = str(float(mLine[4]) + addedTime)
                            # print "part is " + mLine[0]

                            first = 0

                        # if the measurement time stamp is before a segment interval, skip it
                        if float(mLine[4]) < float(currStart):
                            # print("Measurement line starts before adjusted, or is repeated.")
                            # for letter in "iiiiiiiiiiiiiiiiiii":
                            #     print 'error \n'
                            
                            # print "line is " + mLine[0] + ' at ' + mLine[4] + '\n'
                            # print "segment line is " + currStart + ", " + currEnd + ", " + currSegment + '\n'

                            # only read the next line if the parts queue is empty
                            if storage.empty():
                                mLine = next(m).split('\t')
                                mLine = mLine[:-1]

                            # determine what line goes next
                            mLine = get_part(mLine)
                            while mLine == []:
                                mLine = next(m).split('\t')
                                mLine = mLine[:-1]
                                mLine = get_part(mLine)

                            part = float(re.sub(r'.*part(\d{1,2}).mat', r'\1', mLine[0]))
                            addedTime = part * 5000
                            # print "added time is " + str(addedTime) + " for part " + str(part)
                            mLine[4] = str(float(mLine[4]) + addedTime)

                        # gather all measurement lines that are within segment range
                        while float(mLine[4]) >= float(currStart) and float(mLine[4]) <= float(currEnd):
                            # print mLine[4] + " is between currStart: " + currStart + " and currEnd: " + currEnd
                            lines.append(mLine)
                            # only read the next line if the parts queue is empty
                            if storage.empty():
                                mLine = next(m).split('\t')
                                mLine = mLine[:-1]

                            # determine what line goes next
                            mLine = get_part(mLine)
                            while mLine == []:
                                # listy = []
                                # counter = 0
                                # while not storage.empty():
                                #     elem = storage.get()
                                #     listy.append(elem)
                                #     counter += 1
                                #     # print "elem " + str(elem)
                                # # print "length " + str(counter)
                                # for elem in listy:
                                #     storage.put(elem)
                                mLine = next(m).split('\t')
                                # print "next Line " + str(mLine)
                                mLine = mLine[:-1]
                                mLine = get_part(mLine)
                            if mLine == []:
                                print 'ERRORORORORORORORORORORORORORORORRO'
                            
                            part = float(re.sub(r'.*part(\d{1,2}).mat', r'\1', mLine[0]))
                            addedTime = part * 5000
                            # print "added time is " + str(addedTime) + " for part " + str(part)
                            mLine[4] = str(float(mLine[4]) + addedTime)

                        # average line values (except for first two)
                        # print len(mLine)
                        for i in xrange(2, len(mLine)-1, 1):
                            total = float(0.0)
                            counter = 0
                            for mLine in lines:
                                total = total + float(mLine[i])
                                counter = counter + 1

                            # print("counter is " + str(counter) + '\n')
                            # print("total is " + str(total) + '\n')
                            # print(lines)
                            if counter == float(0.0):
                                print lines
                                print "found no lines"
                                print mLine[4]
                                print currSegment
                                print "start " + currStart
                                print "end " + currEnd
                                avg = float(0.0)
                            else:
                                avg = float(total/float(counter))
                            avgline.append(avg)

                        # print all the items in the line
                        for item in avgline:
                            out.write(str(item) + '\t')
                        out.write('\n')
                        # clear variables
                        avgline = []
                        lines = []
                # skip the remaining measurement lines of the file that aren't within a segment
                while name in mLine[0]:
                    # print "skipping extra"
                    mLine = next(m).split('\t')
                    # print mLine[0]

                print "Done with file " + name
                out.close()

# This function is needed because the VoiceSauce built-in .mat to .txt method
# prints files alphabetically into the output file,
# so a file called 'COSPRO_01_F01phr011part11.mat' would be printed before 
# one called 'COSPRO_01_F01phr011part11.mat'. Since we want the parts to be in
# numerical order, the double digit parts are stored until single digit
# parts are all printed
def get_part(line):
    part = float(re.sub(r'.*part(\d{1,2}).mat', r'\1', line[0]))
    if part > float(10):
        # print "part > float(10)"
        storage.put(line)
        return []
    elif part == float(0):
        # print "part == float(0)"
        if storage.empty():
            return line
        else:
            line = storage.get()
            # print "returning " + line
            return 
    else:
        return line


format_files(sys.argv[1], sys.argv[2], sys.argv[3])