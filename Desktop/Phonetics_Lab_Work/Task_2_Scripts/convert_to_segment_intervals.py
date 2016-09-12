#!/usr/bin/python

import sys
import re
from os import listdir, getcwd
from os.path import isfile, relpath, dirname
from itertools import cycle

def format_files(adjusted, otherFile, outpath):

    refdirectory = dirname('/Users/John/Desktop/COSPRO_DATA_BIN/Task2_Formatting')

    if isfile(otherFile):
        if ".txt" in otherFile:
            with open(otherFile, 'r') as m:
                # store header line, remove first two header fields
                header = next(m)
                # print header
                header = header[15:]
                # print "now " + header
    
                # create variables for averaging
                lines = []
                avgline = []
    
                # check if adjusted is a directory
                if isfile(adjusted):
                    print("Please enter a directory of adjusted files.")
    
                # if so, get all files in directory
                files = listdir(adjusted)
    
                # print(files)
                for f in files:
                    # remove adjusted extension
                    name = f[:-9]
                    # print("name is " + name)
                    # .measures is the extension of voicesauce measurements formatted to segment intervals
                    fileTitle = outpath + name + '.measures_aligned'
                    f = adjusted + f
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
                                pieces = re.split(' |\t', line)
                                if len(pieces) > 2:
                                    currStart = pieces[0]
                                    currEnd = pieces[1]
                                    currSegment = pieces[2]
                            except:
                                print("File cannot be split into three parts.\n")
                                print("It is probably either the wrong type of file or was created incorrectly.\n")
                                print "Line is " + line
    
                            if first:
                                # get lines between start and end
                                mLine = next(m).split('\t')
                                # remove newline character for calculations
                                mLine = mLine[:-1]
    
                                # get timestamp of measurements line (adjusted for parts 0-6 if necessary)
                                # each part is up to 5000 milliseconds, so while part 1 says it starts
                                # at 1 millisecond, it really starts at 5001 milliseconds
                                if "part" in mLine[0]:
                                    addedTime = float(re.sub(r'.*part(\d{1,2}).mat', r'\1', mLine[0])) * 10000
                                    mLine[4] = str(float(mLine[4]) + addedTime)
                                    # print "part is " + mLine[0]
                                else:
                                    addedTime = 0.0
    
                                # make sure filenames match up
                                mName = re.sub(r'(.*)part.*', r'\1', mLine[0])
                                while name != mName:
                                    print("Names don't match up")
                                    print "Name is " + name + " but " + mName + " mLine[0] is " + mLine[0] 
                                    mLine = next(m).split('\t')
                                    # remove newline character for calculations
                                    mLine = mLine[:-1]
                                    mName = re.sub(r'(.*)part.*', r'\1', mLine[0])
                                first = 0
    
                            # if the measurement time stamp is before a segment interval, skip it
                            while float(mLine[4]) < float(currStart):
                                print("Measurement line starts before adjusted, or is repeated.")
                                print "line is " + mLine[0] + ' at ' + mLine[4] + '\n'
                                print "segment line is " + currStart + ", " + currEnd + ", " + currSegment + '\n'
                                
                                mLine = next(m).split('\t')
                                mLine = mLine[:-1]
                                # check if file was split into parts
                                if "part" in mLine[0]:
                                    addedTime = float(re.sub(r'.*part(\d{1,2}).mat', r'\1', mLine[0])) * 10000
                                    # print "part is " + mLine[0]
                                else:
                                    addedTime = 0.0
                                # print "added time is " + str(addedTime) + " for part " + str(part)
                                mLine[4] = str(float(mLine[4]) + addedTime)
    
                            # gather all measurement lines that are within segment range
                            while float(mLine[4]) >= float(currStart) and float(mLine[4]) <= float(currEnd):
                                print "file " + mName + " and name " + name
                                print mLine[4] + " is between currStart: " + currStart + " and currEnd: " + currEnd
                                lines.append(mLine)
                                                       
                                # get next line
                                mLine = next(m).split('\t')
                                mLine = mLine[:-1]
                                # check if file was split into parts
                                if "part" in mLine[0]:
                                    addedTime = float(re.sub(r'.*part(\d{1,2}).mat', r'\1', mLine[0])) * 10000
                                    # print "part is " + mLine[0]
                                else:
                                    addedTime = 0.0
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

                            if lines:
                                # start segment should still be the first timestamp
                                first = lines[0]
                                # print first
                                avgline[2] = first[4]
                                # print "time " + lines[0][4]
    
                                # print all the items in the line
                                for item in avgline:
                                    out.write(str(item) + '\t')
                                out.write('\n')
                            # clear variables
                            avgline = []
                            lines = []
                    # skip the remaining measurement lines of the file that aren't within a segment
                    mName = re.sub(r'(.*)part.*', r'\1', mLine[0])
                    while name == mName:
                        print "skipping extra"
                        try:
                            mLine = next(m).split('\t')
                            print "name " + name
                            mName = re.sub(r'(.*)part.*', r'\1', mLine[0])
                            print mLine[4] + ", " + mName
                        except:
                            print "Done with .txt file"
                        # print mLine[0]

                    print "Done with file " + name
                    out.close()
        else:
            print "If outFile is an individual file, it must be measurements (.txt)."
            print "Otherwise outFile should be a directory."
        
    # otherwise, it should be a directory of .creak files
    else: 
        print "directory"

        # check if adjusted is a directory
        if isfile(adjusted):
            print("Please enter a directory of adjusted files.")
            
        # if so, get all files in directory
        aFiles = listdir(adjusted)
        # get file in other directory
        otherFiles = listdir(otherFile)
        # make iterator
        dircycle = cycle(otherFiles)
    
        # create variables for averaging
        lines = float(0)
        counter = 0
        avgline = float(0)

        print "Otherfiles[0] is " + otherFiles[0]

        # check what type of files are in directory
        if ".creak" in otherFiles[0]:
            
            # print(files)
            for f in aFiles:
                # remove adjusted extension
                if "phn" in f:
                    name = f[:-4]
                else:
                    name = f[:-9]
                # print("name is " + name)
                # .measures is the extension of voicesauce measurements formatted to segment intervals
                fileTitle = outpath + name + '.creak_aligned'
                out = open(fileTitle, 'w')
                
                # get absolute path for both files
                # next = otherFile + dircycle.next()
                # print "next is " + next
                currFile = otherFile + dircycle.next()
                # print "currFile is " + currFile
                f = adjusted + f
                # print "f is " + f

                # check that they have the same name
                if name not in currFile:
                    print "Filenames do not match up!"
                with open(currFile, 'r') as c:
                    # skip first line
                    next(c)
    
                    with open(f, 'r') as a:
                        try:
                            # get first two lines
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
                                pieces = re.split(' |\t', line)
                                currStart = pieces[0]
                                currEnd = pieces[1]
                                currSegment = pieces[2]
                            except IOError:
                                print("File cannot be split into three parts.\n")
                                print("It is probably either the wrong type of file or was created incorrectly.\n")
    
                            if first:
                                # get lines between start and end
                                [time, creak] = next(c).split(',')
                                # convert time to milliseconds
                                milltime = 100*float(time)
                                first = 0
    
                            # if the measurement time stamp is before a segment interval, skip it
                            while milltime < float(currStart):
                                print("Creak line starts before adjusted, or is repeated.")
                                print currStart
                                # print "line is " + mLine[0] + ' at ' + mLine[4] + '\n'
                                # print "segment line is " + currStart + ", " + currEnd + ", " + currSegment + '\n'
    
                                try:
                                    cline = next(c)
                                except:
                                    print "No more lines left in creak file."
                                    break

                                [time, creak] = cline.split(',')
                                # convert time to milliseconds
                                milltime = 100*float(time)
    
                            # gather all measurement lines that are within segment range
                            while milltime >= float(currStart) and milltime <= float(currEnd):
                                print "file " + name
                                print str(milltime) + " is between currStart: " + currStart + " and currEnd: " + currEnd
                                lines += float(creak)
                                counter += 1
    
                                try:
                                    cline = next(c)
                                except:
                                    print "No more lines left in creak file."
                                    break

                                [time, creak] = cline.split(',')
                                # convert time to milliseconds
                                milltime = 100*float(time)
    
                            # average creak value
                            # print time range, 
                            if counter != 0:
                                avgline = float(lines / counter)
    
                                out.write(currStart + '\t' + currEnd + '\t' + str(avgline) + '\n')
    
                            # clear variables
                            avgline = float(0)
                            lines = float(0)
                            counter = 0

                    print "Done with file " + name
                    out.close()
        elif ".f0" in otherFiles[0]:
            print "Files are .f0"

            # set counter variables
            totalf0 = float(0)
            totalpm = float(0)

            # print(files)
            for f in aFiles:
                # remove adjusted extension
                if "DS_Store" in f:
                    continue
                if "phn" in f:
                    name = f[:-4]
                else:
                    name = f[:-9]
                # print("name is " + name)
                # .measures is the extension of voicesauce measurements formatted to segment intervals
                fileTitle = outpath + name + '.f0_aligned'
                out = open(fileTitle, 'w')
                
                currFile = otherFile + dircycle.next()
                print "currFile is " + currFile
                f = adjusted + f
                print "f is " + f

                # check that they have the same name
                if name not in currFile:
                    print "Filenames do not match up!"
                with open(currFile, 'r') as c:
                    # skip first 7 lines
                    next(c)
                    next(c)
                    next(c)
                    next(c)
                    next(c)
                    next(c)
                    next(c)
    
                    with open(f, 'r') as a:
                        try:
                            # skip first two lines
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
                                print line
                                print "name is " + name
                                pieces = re.split(' |\t', line)
                                currStart = pieces[0]
                                currEnd = pieces[1]
                                currSegment = pieces[2]
                                print "currStart " + currStart
                                print "currEnd " + currEnd
                                print "currSegment " + currSegment
                            except IOError:
                                print("File cannot be split into three parts.\n")
                                print("It is probably either the wrong type of file or was created incorrectly.\n")
    
                            if first:
                                # get lines between start and end
                                [time, pm, f0] = next(c).split(' ')
                                # convert time to milliseconds
                                milltime = 1000*float(time)
                                first = 0
                            
                            # if the measurement time stamp is before a segment interval, skip it
                            while milltime < float(currStart):
                                print("f0 line starts before adjusted, or is repeated.")
                                print str(milltime) + " is less than " + str(currStart)
                                # print "line is " + mLine[0] + ' at ' + mLine[4] + '\n'
                                # print "segment line is " + currStart + ", " + currEnd + ", " + currSegment + '\n'
    
                                try:
                                    cline = next(c)
                                    print "New " + cline
                                except:
                                    print "No more lines left in f0 file."
                                    break

                                [time, pm, f0] = cline.split(' ')
                                # convert time to milliseconds
                                milltime = 1000*float(time)
    
                            # gather all measurement lines that are within segment range
                            while milltime >= float(currStart) and milltime <= float(currEnd):
                                # print "file " + name
                                # print "pm " + pm + " and f0 " + f0
                                # print str(milltime) + " is between currStart: " + currStart + " and currEnd: " + currEnd
                                totalf0 += float(f0)
                                totalpm += float(pm)
                                counter += 1
    
                                try:
                                    cline = next(c)
                                    print "New " + cline
                                except:
                                    print "No more lines left in creak file."
                                    break

                                [time, pm, f0] = cline.split(' ')
                                # convert time to milliseconds
                                milltime = 1000*float(time)
    
                            # average creak value
                            # print time range, 
                            print "total f0 is " + str(totalf0) + " totalpm is " + str(totalpm) + " counter is " + str(counter)
                            if counter != 0:
                                avgf0 = float(totalf0 / counter)
                                avgpm = float(totalpm / counter)
                                print 'BAGEL'
                                print '================================================================================'
                                print "writing " + currStart + '\t' + currEnd + '\t' + str(avgf0) + '\t' + str(avgpm) + '\n'
                                out.write(currStart + '\t' + currEnd + '\t' + str(avgf0) + '\t' + str(avgpm) + '\n')
                                print '================================================================================'
    
                            # clear variables
                            totalf0 = float(0)
                            totalpm = float(0)
                            counter = 0

                    print "Done with file " + name
                    out.close()

        elif ".pm" in otherFile:
            print "Files are .pm"

            # print(files)
            for f in aFiles:
                # remove adjusted extension
                name = f[:-9]
                # print("name is " + name)
                # .measures is the extension of voicesauce measurements formatted to segment intervals
                fileTitle = outpath + name + '.creak_aligned'
                out = open(fileTitle, 'w')
                
                # open matching .creak file
                currFile = dircycle.next()
                # check that they have the same name
                if name not in currFile:
                    print "Filenames do not match up!"
                with open(otherFile, 'r') as c:
                    # skip first line
                    next(c)
    
                    with open(f, 'r') as a:
                        try:
                            # get first two lines
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
                                [time, creak] = next(c).split(',')
    
                            # if the measurement time stamp is before a segment interval, skip it
                            if float(time) < float(currStart):
                                print("Creak line starts before adjusted, or is repeated.")
                                # print "line is " + mLine[0] + ' at ' + mLine[4] + '\n'
                                # print "segment line is " + currStart + ", " + currEnd + ", " + currSegment + '\n'
    
                                [time, creak] = next(c).split(',')
    
                            # gather all measurement lines that are within segment range
                            while float(time) >= float(currStart) and float(time) <= float(currEnd):
                                # print mLine[4] + " is between currStart: " + currStart + " and currEnd: " + currEnd
                                lines += float(creak)
                                counter += 1
    
                                [time, creak] = next(c).split(',')
    
                            # average creak value
                            # print time range, average
                            avgline = float(lines / counter)
    
                            out.write(currStart + '\t' + currEnd + '\t' + str(avgline) + '\n')
    
                            # clear variables
                            avgline = float(0)
                            lines = float(0)
                            counter = 0
                                
                    # skip the remaining measurement lines of the file that aren't within a segment
                    while name in mLine[0]:
                        print "skipping extra"
                        mLine = next(m).split('\t')
                        # print mLine[0]

                    print "Done with file " + name
                    out.close()

        else:
            print "Directory contains the wrong type of files! (need .creak, .f0 or .pm)"

format_files(sys.argv[1], sys.argv[2], sys.argv[3])