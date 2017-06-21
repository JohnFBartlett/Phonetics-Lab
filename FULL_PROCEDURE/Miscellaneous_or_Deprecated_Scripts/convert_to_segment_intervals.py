#!/usr/bin/python

import sys
import re
from os import listdir, getcwd
from os.path import isfile, relpath, dirname
from itertools import cycle

# THIS SCRIPT IS DEPRECATED - INSTEAD USE convert_to_15_intervals.py
def format_files(partLength, adjusted, otherFile, outpath):

    if isfile(otherFile):
        if ".txt" in otherFile:
            # check that partLength is an integer
            try:
                partLength = int(partLength) * 1000
                print("Part length is " + str(partLength))
            except:
                raise ValueError("Inputted partLength is not an integer.")
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
                    print "current segment file " + f
                    # remove adjusted extension
                    if "DS_Store" in f:
                        continue
                    if "phn" in f:
                        name = f[:-10]
                    else:
                        name = f[:-15]
                    # print("name is " + name)
                    # .measures is the extension of voicesauce measurements formatted to segment intervals
                    fileTitle = outpath + name + '.measures_aligned'
                    f = adjusted + f
                    out = open(fileTitle, 'w')
    
                    #write header
                    out.write(header)
    
                    with open(f, 'r') as a:
                        skip_a = False
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
                                    addedTime = float(re.sub(r'.*part(\d{1,2}).mat', r'\1', mLine[0])) * partLength
                                    mLine[4] = str(float(mLine[4]) + addedTime)
                                    # print "part is " + mLine[0]

                                    # also set mName accounting for "partxx" addition
                                    # print mLine[0]
                                    # print "transform"
                                    mName = re.sub(r'(.*)part.*', r'\1', mLine[0])
                                    # print mName
                                else:
                                    addedTime = 0.0
                                    mName = mLine[0][:-4]
    
                                # make sure filenames match up
                                while name != mName:
                                    print("Names don't match up")
                                    print "Name is " + name + " but " + mName + " mLine[0] is " + mLine[0] 
                                    
                                    # decide which file to skip a line from
                                    skip_a = choose_skip_line(name, mName)

                                    if not skip_a:
                                        print "Skipping measure " + mName
                                        # if "part" in mLine[0]:
                                        #     addedTime = float(re.sub(r'.*part(\d{1,2}).mat', r'\1', mLine[0])) * partLength
                                        #     mLine[4] = str(float(mLine[4]) + addedTime)
                                        # # print "part is " + mLine[0]
                                        # print("time " + mLine[4])
                                        while mName in mLine[0]:
                                            mLine = next(m).split('\t')
                                        print("finished skipping, " + mName + " no longer in " + mLine[0])
                                        # remove newline character for calculations
                                        mLine = mLine[:-1]
                                        if "part" in mLine[0]:
                                            mName = re.sub(r'(.*)part.*', r'\1', mLine[0])
                                        else:
                                            mName = mLine[0][:-4]
                                    else:
                                        print "Skipping adjusted " + name
                                        break
                                first = 0
    
                            if skip_a:
                                # break out of for loop, go to next file
                                print("Skipping rest of " + name)
                                break
                            # if the measurement time stamp is before a segment interval, skip it
                            while float(mLine[4]) < float(currStart):
                                print("Measurement line starts before adjusted, or is repeated.")
                                print "line is " + mLine[0] + ' at ' + mLine[4] + '\n'
                                print "segment line is " + currStart + ", " + currEnd + ", " + currSegment + '\n'
                                
                                try:
                                    mLine = next(m).split('\t')
                                except:
                                    print "Done with .txt file"
                                    break
                                mLine = mLine[:-1]
                                # check if file was split into parts
                                if "part" in mLine[0]:
                                    addedTime = float(re.sub(r'.*part(\d{1,2}).mat', r'\1', mLine[0])) * partLength
                                    print "part is " + mLine[0]
                                else:
                                    addedTime = 0.0
                                # print "added time is " + str(addedTime) + " for part " + str(part)
                                mLine[4] = str(float(mLine[4]) + addedTime)
    
                            # gather all measurement lines that are within segment range
                            while float(mLine[4]) >= float(currStart) and float(mLine[4]) <= float(currEnd):
                                # print "file " + mName + " and name " + name
                                # print mLine[4] + " is between currStart: " + currStart + " and currEnd: " + currEnd
                                lines.append(mLine)
                                                       
                                # get next line
                                try:
                                    mLine = next(m).split('\t')
                                except:
                                    print "Done with .txt file"
                                    break
                                mLine = mLine[:-1]
                                # check if file was split into parts
                                if "part" in mLine[0]:
                                    addedTime = float(re.sub(r'.*part(\d{1,2}).mat', r'\1', mLine[0])) * partLength
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
                    if "part" in mLine[0]:
                        mName = re.sub(r'(.*)part.*', r'\1', mLine[0])
                    else:
                        mName = mLine[0][:-4]
                    while name == mName:
                        # print name + ", " + mName
                        # print "skipping extra"
                        try:
                            mLine = next(m).split('\t')
                            # print "name " + name
                            # print mLine[4] + ", " + mName
                            if "part" in mLine[0]:
                                mName = re.sub(r'(.*)part.*', r'\1', mLine[0])
                            else:
                                mName = mLine[0][:-4]
                            # print mLine[4] + ", " + mName
                        except:
                            print "Done with .txt file"
                            break
                        # print mLine[0]
                    print "Done with file " + name
                    # print name + " no longer matches  mName " + mName
                    out.close()
        else:
            print "If outFile is an individual file, it must be measurements (.txt)."
            print "Otherwise outFile should be a directory."
 
# ====================================================================       
    # DIRECTORY SECTION
# ====================================================================

    # otherwise, it should be a directory of .creak files
    else: 
        print "directory"

        # check if adjusted is a directory
        if isfile(adjusted):
            print("Please enter a directory of adjusted files.")
            
        # if so, get all files in directory
        aFiles = listdir(adjusted)
        print aFiles
        # get file in other directory
        otherFiles = listdir(otherFile)
        print "oth is " + str(otherFiles)
        # make iterator
        dircycle = cycle(otherFiles)
    
        # create variables for averaging
        lines = float(0)
        counter = 0
        avgline = float(0)

        print "Otherfiles[3] is " + otherFiles[1]

        # check what type of files are in directory
        if ".creak" in otherFiles[1]:
            
            # boolean that says whether to skip the rest of the adjusted file
            skip_a = False
            currName = ''

            # print(files)
            for f in aFiles:
                # remove adjusted extension
                if "DS_Store" in f:
                    continue
                if "phn" in f:
                    name = f[:-10]
                else:
                    name = f[:-15]
                # print("name is " + name)
                
                # # only get the next .creak file if an adjusted is not being skipped
                # if not skip_a:
                #     # print "Getting next creak"
                #     # currFile = otherFile + dircycle.next()
                #     # if "DS_Store" in currFile:
                #     #     currFile = otherFile + dircycle.next()
                #     # currName = re.sub(r'.*/(.*)', r'\1', currFile[:-6])
                #     # # print "currFile is " + currFile
                #     # # print "currName is " + currName
                # else:
                #     skip_a = False
                f = adjusted + f
                # print "f is " + f

                # check that they have the same name
                while name != currName:
                    # print "==========================="
                    # print "Filenames do not match up!"
                    # print "name is " + name + " and currName is " + currName
                    # print "==========================="
                    skip_a = choose_skip_line(name, currName)
                    # go to the next adjusted file if skip_a is true
                    if skip_a:
                        print "Skipping adjusted file."  + name
                        break
                    # otherwise go to the next .creak file instead
                    else:
                        print "Skipping .creak file." + currName
                        currFile = otherFile + dircycle.next()
                        currName = re.sub(r'.*/(.*)', r'\1', currFile[:-6])
                else:
                    print "Name " + name + " matches creakName " + currName
                if skip_a:
                    # go to next iteration
                    continue

                # if they match up, create out file (if it's the first part)
                fileTitle = outpath + name + '.creak_aligned'
                out = open(fileTitle, 'w')

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
                                milltime = 1000*float(time)
                                first = 0
    
                            # if the measurement time stamp is before a segment interval, skip it
                            while milltime < float(currStart):
                                print("Creak line starts before adjusted, or is repeated.")
                                print currStart
                                print "milltime is " + str(milltime)
                                print "segment line is " + currStart + ", " + currEnd + ", " + currSegment + '\n'
    
                                try:
                                    cline = next(c)
                                    print "new line is " + cline
                                except:
                                    print "No more lines left in creak file."
                                    break

                                [time, creak] = cline.split(',')
                                # convert time to milliseconds
                                milltime = 1000*float(time)
    
                            # gather all measurement lines that are within segment range
                            while milltime >= float(currStart) and milltime <= float(currEnd):
                                # print "file " + name
                                # print str(milltime) + " is between currStart: " + currStart + " and currEnd: " + currEnd
                                lines += float(creak)
                                counter += 1
    
                                try:
                                    cline = next(c)
                                except:
                                    print "No more lines left in creak file."
                                    break

                                [time, creak] = cline.split(',')
                                # convert time to milliseconds
                                milltime = 1000*float(time)
    
                            # average creak value
                            # print time range, 
                            if counter != 0:
                                avgline = float(lines / counter)
                                print("=====================================")
                                print("Writing Line: " + currStart + '\t' + currEnd + '\t' + str(avgline))
                                print("=====================================")
                                out.write(currStart + '\t' + currEnd + '\t' + str(avgline) + '\n')
                            # if there are no creak lines within the range
                            # which would be if the segment interval is too small,
                            # just take the previous creak line -- it should be very close
                            else:
                                print "NO CREAK LINE BETWEEN INTERVAL, taking previous."
                                print("=====================================")
                                print("Writing Line: " + currStart + '\t' + currEnd + '\t' + str(float(creak)))
                                print("=====================================")
                                out.write(currStart + '\t' + currEnd + '\t' + str(float(creak)) + '\n')
    
                            # clear variables
                            avgline = float(0)
                            lines = float(0)
                            counter = 0

                    print "Done with file " + name
                    out.close()
        elif ".f0" in otherFiles[3]:
            print "Files are .f0"

            # set counter variables
            totalf0 = float(0)
            totalpm = float(0)

            # boolean that says whether to skip the rest of the adjusted file
            skip_a = False
            # get first
            currFile = otherFile + dircycle.next()
            currName = re.sub(r'.*/(.*)', r'\1', currFile[:-3])
            print "currName " + currName

            # print(files)
            for f in aFiles:

                # remove adjusted extension
                if "DS_Store" in f:
                    continue
                if ".pm" in f:
                    continue
                if "phn" in f:
                    name = f[:-10]
                else:
                    name = f[:-15]
                # print("name is " + name)
                
                # # only get the next .f0 file if an adjusted is not being skipped
                # if not skip_a:
                #     print "--------------------------------------------"
                #     print "Getting next f0"
                #     currFile = otherFile + dircycle.next()
                #     currName = re.sub(r'.*/(.*)', r'\1', currFile[:-3])
                #     # print "currFile is " + currFile
                #     # print "currName is " + currName
                # else:
                #     skip_a = False
                f = adjusted + f
                # # print "f is " + f

                # check that they have the same name
                while name != currName:
                    # print "==========================="
                    # print "Filenames do not match up!"
                    # print "name is " + name + " and currName is " + currName
                    # print "==========================="
                    skip_a = choose_skip_line(name, currName)
                    # go to the next adjusted file if skip_a is true
                    if skip_a:
                        print "Skipping adjusted file " + name
                        break
                    # otherwise go to the next .creak file instead
                    else:
                        print "Skipping .f0 file " + currName
                        currFile = otherFile + dircycle.next()
                        currName = re.sub(r'.*/(.*)', r'\1', currFile[:-3])
                else:
                    print "Name " + name + " matches creakName " + currName
                if skip_a:
                    # go to next iteration
                    continue

                # if they match up, create out file
                fileTitle = outpath + name + '.f0_aligned'
                out = open(fileTitle, 'w')

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
                                # print line
                                # print "name is " + name
                                pieces = re.split(' |\t', line)
                                currStart = pieces[0]
                                currEnd = pieces[1]
                                currSegment = pieces[2]
                                # print "currStart " + currStart
                                # print "currEnd " + currEnd
                                # print "currSegment " + currSegment
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
                                    # print "next line" + cline
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
                                    # print "next line " + cline
                                except:
                                    print "No more lines left in f0 file."
                                    break

                                [time, pm, f0] = cline.split(' ')
                                # convert time to milliseconds
                                milltime = 1000*float(time)
                                # print milltime
    
                            # average creak value
                            # print time range, 
                            # print "total f0 is " + str(totalf0) + " totalpm is " + str(totalpm) + " counter is " + str(counter)
                            if counter != 0:
                                avgf0 = float(totalf0 / counter)
                                avgpm = float(totalpm / counter)
                                # print '================================================================================'
                                # print "writing " + currStart + '\t' + currEnd + '\t' + str(avgf0) + '\t' + str(avgpm) + '\n'
                                out.write(currStart + '\t' + currEnd + '\t' + str(avgf0) + '\t' + str(avgpm) + '\n')
                                # print '================================================================================'
    
                            # clear variables
                            totalf0 = float(0)
                            totalpm = float(0)
                            counter = 0

                    print "Done with file " + name
                    out.close()

        # elif ".pm" in otherFile:
        #     print "Files are .pm"

        #     # print(files)
        #     for f in aFiles:
        #         # remove adjusted extension
        #         name = f[:-9]
        #         # print("name is " + name)
        #         # .measures is the extension of voicesauce measurements formatted to segment intervals
        #         fileTitle = outpath + name + '.creak_aligned'
        #         out = open(fileTitle, 'w')
                
        #         # open matching .creak file
        #         currFile = otherFile + dircycle.next()
        #         currName = currFile[:-3]
        #         # print "currFile is " + currFile
        #         f = adjusted + f
        #         # print "f is " + f

        #         # check that they have the same name
        #         if name != currName:
        #             print "Filenames do not match up!"
        #         with open(otherFile, 'r') as c:
        #             # skip first line
        #             next(c)
    
        #             with open(f, 'r') as a:
        #                 try:
        #                     # get first two lines
        #                     next(a)
        #                     next(a)
        #                 except IOError:
        #                     print("File has fewer than two lines of content.\n")
        #                     print("It is probably either the wrong type of file or was created incorrectly.\n")
        #                 # look at one line at a time
        #                 first = 1
        #                 for line in a:
        #                     try:
        #                         # print "A line is " + line
        #                         [currStart, currEnd, currSegment] = line.split(' ')
        #                     except IOError:
        #                         print("File cannot be split into three parts.\n")
        #                         print("It is probably either the wrong type of file or was created incorrectly.\n")
    
        #                     if first:
        #                         # get lines between start and end
        #                         [time, creak] = next(c).split(',')
    
        #                     # if the measurement time stamp is before a segment interval, skip it
        #                     if float(time) < float(currStart):
        #                         print("Creak line starts before adjusted, or is repeated.")
        #                         # print "line is " + mLine[0] + ' at ' + mLine[4] + '\n'
        #                         # print "segment line is " + currStart + ", " + currEnd + ", " + currSegment + '\n'
    
        #                         [time, creak] = next(c).split(',')
    
        #                     # gather all measurement lines that are within segment range
        #                     while float(time) >= float(currStart) and float(time) <= float(currEnd):
        #                         # print mLine[4] + " is between currStart: " + currStart + " and currEnd: " + currEnd
        #                         lines += float(creak)
        #                         counter += 1
    
        #                         [time, creak] = next(c).split(',')
    
        #                     # average creak value
        #                     # print time range, average
        #                     avgline = float(lines / counter)
    
        #                     out.write(currStart + '\t' + currEnd + '\t' + str(avgline) + '\n')
    
        #                     # clear variables
        #                     avgline = float(0)
        #                     lines = float(0)
        #                     counter = 0
                                
        #             # skip the remaining measurement lines of the file that aren't within a segment
        #             while name in mLine[0]:
        #                 print "skipping extra"
        #                 mLine = next(m).split('\t')
        #                 # print mLine[0]

        #             print "Done with file " + name
        #             out.close()

        else:
            print "Directory contains the wrong type of files! (need .creak, .f0 or .pm)"

def choose_skip_line(adjName, mName):
    # determine whether a line in adjusted or in measures should be skipped
    # do this by getting gradient numbers and skipping the one that is more behind
    try:
        adjValues = re.sub(r'.*_\d{2}_(\w)(\d{2,4})(\w+?)(\d{3,4}).*', r'\1 \2 \3 \4', adjName)
        [adjgender, adjspeakId, adjfiletype, adjnum] = adjValues.split(' ')
        adjTypeNo = ''
        if '_d' in adjName:
            adjTypeNo = 0
        elif '_e' in adjName:
            adjTypeNo = 1
        elif '_i' in adjName:
            adjTypeNo = 2
    except:
        # if it doesn't fit the regex, skip it
        return True
    try:
        mValues = re.sub(r'.*_\d{2}_(\w)(\d{3,4})(\w+?)(\d{3,4}).*', r'\1 \2 \3 \4', mName)
        [mgender, mspeakId, mfiletype, mnum] = mValues.split(' ')
        mTypeNo = ''
        if '_d' in mName:
            mTypeNo = 0
        elif '_e' in mName:
            mTypeNo = 1
        elif '_i' in mName:
            mTypeNo = 2
    except:
        # if it doesn't fit the regex, skip it
        return False
    # print(adjspeakId + ',' + adjfiletype + ',' + adjnum)
    # print(mspeakId + ',' + mfiletype + ',' + mnum)

    # see if they are the same gender
    if adjgender == mgender:
        # see if they are the same speaker
        if int(adjspeakId) == int(mspeakId):
            # see if they are the same filetype (phr vs. w vs. prg.)
            if adjfiletype == mfiletype:
                # see if they are they same file number
                if int(adjnum) == int(mnum):
                    if adjTypeNo == mTypeNo:
                        if mName != re.sub(r'.*prg\d+(_.)', r'\1', mName):
                            print "skipping " + mName
                            return False
                        raise ValueError("I don't know which file to skip!")
                    elif adjTypeNo < mTypeNo:
                        return True
                    else:
                        return False
                # see if adj is prev file number
                elif int(adjnum) < int(mnum):
                    # skip adj file
                    print(adjspeakId + ',' + adjfiletype + ',' + adjnum + ' (a) is before ' + mspeakId + ',' + mfiletype + ',' + mnum)
                    return True
                # see if mLine is a prev file number
                else:
                    # skip mLine
                    # print(mspeakId + ',' + mfiletype + ',' + mnum + ' (m) is before ' + adjspeakId + ',' + adjfiletype + ',' + adjnum)
                    return False
            # skip whichever one is word or prg (this needs to be done in cospro02 sometimes)
            elif 'w' in adjfiletype or 'prg' in adjfiletype:
                # skip adj file
                print(adjspeakId + ',' + adjfiletype + ',' + adjnum + ' (a) is before ' + mspeakId + ',' + mfiletype + ',' + mnum)
                return True
            # see if mLine is a prev speaker 
            elif 'w' in mfiletype or 'prg' in filetype:
                # skip mLine
                # print(mspeakId + ',' + mfiletype + ',' + mnum + ' (m) is before ' + adjspeakId + ',' + adjfiletype + ',' + adjnum)
                return False
            else:
                raise ValueError("I dont know which file to skip!")
        #see if adj is a prev speaker
        elif int(adjspeakId) < int(mspeakId):
            # skip adj file
            print(adjspeakId + ',' + adjfiletype + ',' + adjnum + ' (a) is before ' + mspeakId + ',' + mfiletype + ',' + mnum)
            return True
        # see if mLine is a prev speaker 
        else:
            # skip mLine
            # print(mspeakId + ',' + mfiletype + ',' + mnum + ' (m) is before ' + adjspeakId + ',' + adjfiletype + ',' + adjnum)
            return False
    # if adj is F, skip it (because F comes first)
    elif adjgender == 'F':
        # skip adj file
        print(adjspeakId + ',' + adjfiletype + ',' + adjnum + ' (a) is before ' + mspeakId + ',' + mfiletype + ',' + mnum)
        return True
    # otherwise adj is probably 'M' and m is 'F' 
    else:
        # skip mLine
        # print(mspeakId + ',' + mfiletype + ',' + mnum + ' (m) is before ' + adjspeakId + ',' + adjfiletype + ',' + adjnum)
        return False


refdirectory = dirname('/Users/John/Desktop/COSPRO_DATA_BIN/Task2_Formatting/')
if sys.argv[1] == 'creak':
    if not 'COSPRO_0' in sys.argv[2]:
        raise ValueError("Wrong input.")
    segAddress = refdirectory + '/2-Formatted_Segments/' + sys.argv[2]
    print segAddress
    creakAddress = refdirectory + '/1-Raw_Creaks/' + sys.argv[2]
    outAddress = refdirectory + '/2-Formatted_Creak/' + sys.argv[2]
    format_files(sys.argv[3], segAddress, creakAddress, outAddress)
elif sys.argv[1] == 'reaper':
    if not 'COSPRO_0' in sys.argv[2]:
        raise ValueError("Wrong input.")
    segAddress = refdirectory + '/2-Formatted_Segments/' + sys.argv[2]
    print segAddress
    reapAddress = refdirectory + '/1-Raw_Reaper_Results/' + sys.argv[2]
    outAddress = refdirectory + '/2-Formatted_Reaper_Results/' + sys.argv[2]
    format_files(sys.argv[3], segAddress, reapAddress, outAddress)
else:
    format_files(sys.argv[4], sys.argv[1], sys.argv[2], sys.argv[3])
