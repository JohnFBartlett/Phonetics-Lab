#!/usr/bin/python

import sys
import re

from os import listdir, getcwd
from os.path import isfile, relpath, dirname
from itertools import cycle

def format_files(partLength, adjusted, otherFile, outpath):


# ====================================================================       
    # DIRECTORY SECTION
# ====================================================================

    # otherwise, it should be a directory of .creak files
    if not isfile(otherFile): 
        print("directory")

        # check if adjusted is a directory
        if isfile(adjusted):
            print("Please enter a directory of adjusted files.")
            
        # if so, get all files in directory
        aFiles = listdir(adjusted)
        # print aFiles
        # get file in other directory
        otherFiles = listdir(otherFile)
        # print "oth is " + str(otherFiles)
        # make iterator
        dircycle = cycle(otherFiles)
    
        # create variables for averaging
        lines = []
        counter = 0
        avgline = float(0)

        print("Otherfiles[1] is " + otherFiles[1])

        # check what type of files are in directory
        if ".creak" in otherFiles[1]:
            
            # boolean that says whether to skip the rest of the adjusted file
            skip_a = False
            currName = ''

            # print(files)
            for f in aFiles:
                # remove adjusted extension
                if "DS" in f:
                    continue
                if "phn" in f:
                    name = f[:-10]
                else:
                    name = f[:-15]
                # print("name is " + name)
                
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
                        # print("Does not match " + currName)
                        # print("Skipping adjusted file "  + name)
                        break
                    # otherwise go to the next .creak file instead
                    else:
                        # print("Does not match " + name)
                        # print("Skipping .creak file." + currName)
                        currFile = otherFile + next(dircycle)
                        currName = re.sub(r'.*/(.*)', r'\1', currFile[:-6])
                # else:
                #     # print("Name " + name + " matches creakName " + currName)
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
                                # print("Creak line starts before adjusted, or is repeated.")
                                # print(currStart)
                                # print("milltime is " + str(milltime))
                                # print("segment line is " + currStart + ", " + currEnd + ", " + currSegment + '\n')
    
                                try:
                                    cline = next(c)
                                    # print("new line is " + cline)
                                except:
                                    # print("No more lines left in creak file.")
                                    break

                                [time, creak] = cline.split(',')
                                # convert time to milliseconds
                                milltime = 1000*float(time)
    
                            # gather all measurement lines that are within segment range
                            while milltime >= float(currStart) and milltime <= float(currEnd):
                                # print "file " + name
                                # print(str(milltime) + " is between currStart: "
                                # + currStart + " and currEnd: " + currEnd)
                                lines.append([milltime, float(creak)])
                                counter += 1
    
                                try:
                                    cline = next(c)
                                except:
                                    # print("No more lines left in creak file.")
                                    break

                                [time, creak] = cline.split(',')
                                # convert time to milliseconds
                                milltime = 1000*float(time)
    
                            # average creak value
                            # print time range, 
                            if counter != 0:
                                creak_averages = IntervalCalculator.calculate_interval_values(float(currStart),
                                                                                              float(currEnd), lines)
                                out.write(currStart + '\t' + currEnd + '\t')
                                # goes to 16 instead of 15 because the first value is the average
                                for i in range(16):
                                    out.write(str(creak_averages[i]))
                                    if i < 15:
                                        out.write('\t')
                                out.write('\n')

                            # if there are no creak lines within the range
                            # which would be if the segment interval is too small,
                            # just take the previous creak line -- it should be very close
                            else:
                                # print("NO CREAK LINE BETWEEN INTERVAL, taking previous.")
                                # print("=====================================")
                                # print("Writing Line: " + currStart + '\t' + currEnd + '\t' + str(float(creak)))
                                # print("=====================================")
                                out.write(currStart + '\t' + currEnd + '\t' + str(float(creak)) + '\t')
                                for i in range(15):
                                    out.write(str(float(creak)))
                                    if i < 14:
                                        out.write('\t')
                                out.write('\n')
    
                            # clear variables
                            avgline = float(0)
                            lines = []
                            counter = 0

                    print("Formatted file " + name)
                    out.close()
        elif ".f0" in otherFiles[1]:
            print("Files are .f0")
            # print(otherFiles)
            # boolean that says whether to skip the rest of the adjusted file
            skip_a = False
            # get first
            currFile = otherFile + next(dircycle)
            currName = re.sub(r'.*/(.*)', r'\1', currFile[:-3])
            print("currName " + currName)

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
                        # print("Skipping adjusted file " + name)
                        # print("Does not match " + currName)
                        break
                    # otherwise go to the next .creak file instead
                    else:
                        # print("Skipping .f0 file " + currName)
                        # print("Does not match " + name)
                        currFile = otherFile + next(dircycle)
                        currName = re.sub(r'.*/(.*)', r'\1', currFile[:-3])
                # else:
                #     # print("Name " + name + " matches creakName " + currName)
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
                                # print("f0 line starts before adjusted, or is repeated.")
                                # print str(milltime) + " is less than " + str(currStart)
                                # print "line is " + mLine[0] + ' at ' + mLine[4] + '\n'
                                # print "segment line is " + currStart + ", " + currEnd + ", " + currSegment + '\n'
    
                                try:
                                    cline = next(c)
                                    # print "next line" + cline
                                except:
                                    # print("No more lines left in f0 file.")
                                    break

                                [time, pm, f0] = cline.split(' ')
                                # convert time to milliseconds
                                milltime = 1000*float(time)
    
                            # gather all measurement lines that are within segment range
                            while milltime >= float(currStart) and milltime <= float(currEnd):
                                # print "file " + name
                                # print "pm " + pm + " and f0 " + f0
                                # print str(milltime) + " is between currStart: " + currStart + " and currEnd: " + currEnd
                                lines.append([milltime, float(f0), float(pm)])
                                counter += 1
    
                                try:
                                    cline = next(c)
                                    # print "next line " + cline
                                except:
                                    # print("No more lines left in f0 file.")
                                    break

                                [time, pm, f0] = cline.split(' ')
                                # convert time to milliseconds
                                milltime = 1000*float(time)
                                # print milltime
    
                            # average f0 value
                            if counter != 0:
                                f0_averages = IntervalCalculator.calculate_f0_interval_values(float(currStart), float(currEnd), lines)
                                out.write(currStart + '\t' + currEnd + '\t')
                                # goes to 32 bc of f0 and pm averages plus intervals
                                for i in range(32):
                                    try:
                                        out.write(str(f0_averages[i]))
                                    except:
                                        print("Not enough values in creak list!")
                                    if i < 32:
                                        out.write('\t')
                                out.write('\n')
    
                            else:
                                # print("NO f0 LINE BETWEEN INTERVAL, taking previous.")
                                # print("=====================================")
                                # print("Writing Line: " + currStart + '\t' + currEnd + '\t' + str(float(f0)) + '\t' + str(float(pm)))
                                # print("=====================================")
                                out.write(currStart + '\t' + currEnd + '\t' + str(avgf0) + '\t')
                                for i in range(15):
                                    out.write(str(avgf0))
                                    if i < 14:
                                        out.write('\t')
                                out.write(str(avgpm) + '\t')
                                for i in range(15):
                                    out.write(str(avgpm))
                                    if i < 14:
                                        out.write('\t')
                                out.write('\n')

                            # clear variables
                            lines = []
                            avgpm = 0
                            avgf0 = 0
                            counter = 0

                    print("Formatted file " + name)
                    out.close()
        else:
            print("Directory contains the wrong type of files! (need .creak, .f0 or .pm)")

# for choosing which file to skip among files from the Children's corpus
# returning trur means the adjusted file should be skipped,
# false means the other file should be skipped
# sample c_f_svo_a10_s2_p01_t035_svo_r1.measures_aligned
def choose_skip_lineCC(adjName, mName):
    try:
        adjValues = re.sub(r'.*_a([\d\w]{1,2})_s(\d)_p(\d+)_t(\d+)_.*', r'\1 \2 \3 \4', adjName)
        [adjage, adjsample, adjperson, adjnum] = adjValues.split(' ')
        if 'a' in adjage:
            adjage = 20
    except: 
        return True

    try:
        mValues = re.sub(r'.*_a([\d\w]{1,2})_s(\d)_p(\d+)_t(\d+)_.*', r'\1 \2 \3 \4', mName)
        [mage, msample, mperson, mnum] = mValues.split(' ')
        if 'a' in mage:
            mage = 20
    except: 
        return False

    # see if they are the same age
    if int(adjage) == int(mage):
        # see if they are the same sample
        if int(adjsample) == int(msample):
            # see if they are the same person
            if int(adjperson) == int(mperson):
                # see if they are they same file number
                if int(adjnum) == int(mnum):
                    print("adjusted file: " + adjName + ", other file: " + mName)
                    raise ValueError("Can't tell which file to skip!")
                elif int(adjnum) < int(mnum):
                    return True
                else:
                    return False
            elif int(adjperson) < int(mperson):
                return True
            else:
                return False
        elif int(adjsample) < int(msample):
            return True
        else:
            return False
    elif int(adjage) < int(mage):
        return True
    else:
        return False

# determine whether a line in adjusted or in measures should be skipped
# do this by getting gradient numbers and skipping the one that is more behind
def choose_skip_line(adjName, mName):
    try:
        adjValues = re.sub(r'.*_\d{2}_(\w{1,2})(\d{2,4})(\w+?)(\d{3,4}).*', r'\1 \2 \3 \4', adjName)
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
        print("Failed COSPRO comparison: " + adjName)
        return choose_skip_lineCC(adjName, mName)
    try:
        mValues = re.sub(r'.*_\d{2}_(\w{1,2})(\d{2,4})(\w+?)(\d{3,4}).*', r'\1 \2 \3 \4', mName)
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
        print("Failed COSPRO comparison: " + mName)
        return False
    # print(adjspeakId + ',' + adjfiletype + ',' + adjnum)
    # print(mspeakId + ',' + mfiletype + ',' + mnum)

    # see if they are the same gender
    if adjgender in mgender:
        # print('check1 gender is same')
        # see if they are the same speaker
        if int(adjspeakId) == int(mspeakId):
            # print('check2 is same')
            # see if they are the same filetype (phr vs. w vs. prg.)
            if adjfiletype in mfiletype:
                # print('check3 type is same')
                # see if they are they same file number
                if int(adjnum) == int(mnum):
                    if adjTypeNo == mTypeNo:
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
            # CHANGED: w < phr < prg
            elif 'w' in adjfiletype:
                # skip adj file
                print(adjspeakId + ',' + adjfiletype + ',' + adjnum + ' (a) is before ' + mspeakId + ',' + mfiletype + ',' + mnum)
                return True
            # see if mLine is a prev speaker 
            elif 'w' in mfiletype:
                # skip mLine
                # print(mspeakId + ',' + mfiletype + ',' + mnum + ' (m) is before ' + adjspeakId + ',' + adjfiletype + ',' + adjnum)
                return False
            elif 'prg' in adjfiletype:
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
    elif 'F' in adjgender:
        # skip adj file
        print(adjspeakId + ',' + adjfiletype + ',' + adjnum + ' (a) is before ' + mspeakId + ',' + mfiletype + ',' + mnum)
        return True
    # otherwise adj is probably 'M' and m is 'F' 
    else:
        # skip mLine
        # print(mspeakId + ',' + mfiletype + ',' + mnum + ' (m) is before ' + adjspeakId + ',' + adjfiletype + ',' + adjnum)
        return False


class IntervalCalculator:
    # takes in the start time of a segment, the end time of the same segment,
    # and the list of creak values (paired with their timestamps)
    # that fall within the segment's start and end times
    #
    # returns an array containing the overall average creak value followed
    # by the 15 interval averages for the given segment
    @staticmethod
    def calculate_interval_values(startTime, endTime, creakList):
        output = []
        # print(creakList)
        # first get average
        just_vals = [elem[1] for elem in creakList]
        avg_val = sum(just_vals) / float(len(just_vals))
        output.append(avg_val)

        interval = (endTime - startTime) / 15.0
        creaks = iter(creakList)
        prev = ''
        curr = next(creaks)
        # print('Curr: ' + str(curr))
        for i in range(0, 15):
            startInterval = startTime + i * interval
            endInterval = startTime + (i + 1) * interval
            tempList = []
            while curr[0] < endInterval and curr[0] >= startInterval:
                tempList.append(curr[1])
                prev = curr
                try:
                    curr = next(creaks)
                except StopIteration:
                    break
            if not tempList:
                if not prev:
                    tempList.append(curr[1])
                else:
                    middle = startInterval + interval / 2
                    if abs(middle - prev[0]) < abs(curr[0] - middle):
                        tempList.append(prev[1])
                    else:
                        tempList.append(curr[1])
            # print("List of values for interval " + str(i) + ": " + str(tempList))
            interval_entry = float(sum(tempList)) / float(len(tempList))
            # print("Interval entry = " + str(interval_entry))
            output.append(interval_entry)
        # print("Printing output")
        # print(output)
        return output

    @staticmethod
    def calculate_f0_interval_values(startTime, endTime, valuesList):
        output = []
        # print(valuesList)
        # print('Getting f0 averages.')
        # first get average
        f0_vals = [elem[1] for elem in valuesList]
        avg_f0_val = sum(f0_vals) / float(len(f0_vals))
        output.append(avg_f0_val)

        interval = (endTime - startTime) / 15.0
        values = iter(valuesList)
        prev = ''
        curr = next(values)
        # print('Curr: ' + str(curr))
        for i in range(0, 15):
            startInterval = startTime + i * interval
            endInterval = startTime + (i + 1) * interval
            tempList = []
            while endInterval > curr[0] >= startInterval:
                tempList.append(curr[1])
                prev = curr
                try:
                    curr = next(values)
                except StopIteration:
                    break
            if not tempList:
                if not prev:
                    tempList.append(curr[1])
                else:
                    middle = startInterval + interval / 2
                    if abs(middle - prev[0]) < abs(curr[0] - middle):
                        tempList.append(prev[1])
                    else:
                        tempList.append(curr[1])
            # print("List of values for interval " + str(i) + ": " + str(tempList))
            interval_entry = float(sum(tempList)) / float(len(tempList))
            # print("Interval entry = " + str(interval_entry))
            output.append(interval_entry)

        # print('Getting pitchmark averages.')
        try:
            pm_vals = [elem[2] for elem in valuesList]
            avg_pm_val = sum(pm_vals) / float(len(pm_vals))
            output.append(avg_pm_val)
        except:
            print("Input doesn't have pm column!")
            return None

        interval = (endTime - startTime) / 15.0
        values = iter(valuesList)
        prev = ''
        curr = next(values)
        for i in range(0, 15):
            startInterval = startTime + i * interval
            endInterval = startTime + (i + 1) * interval
            tempList = []
            while endInterval > curr[0] >= startInterval:
                tempList.append(curr[2])
                prev = curr
                try:
                    curr = next(values)
                except StopIteration:
                    break
            if not tempList:
                if not prev:
                    tempList.append(curr[2])
                else:
                    middle = startInterval + interval / 2
                    if abs(middle - prev[0]) < abs(curr[0] - middle):
                        tempList.append(prev[2])
                    else:
                        tempList.append(curr[2])
            # print("List of values for interval " + str(i) + ": " + str(tempList))
            interval_entry = float(sum(tempList)) / float(len(tempList))
            # print("Interval entry = " + str(interval_entry))
            output.append(interval_entry)
        # print("Printing output")
        # print(output)
        return output

if __name__ == '__main__':
    # sample command python ~/Desktop/Phonetics_Lab_Work/Task_2_Scripts/convert_to_15_intervals.py creak COSPRO_01/ 10
    refdirectory = dirname('/Users/John/Documents/Phonetics_Lab_Summer_2017/'
                           'Phonetics-Lab/COSPRO_DATA_BIN/data_analysis/')
    if sys.argv[1] == 'creak':
        if not 'COSPRO_0' in sys.argv[2]:
            if not 'Child' in sys.argv[2]:
                print(sys.argv[2])
                raise ValueError("Wrong input.")
        segAddress = refdirectory + '/2-Formatted_Segments/' + sys.argv[2]
        print(segAddress)
        creakAddress = refdirectory + '/1-Raw_Creaks/' + sys.argv[2]
        outAddress = refdirectory + '/2-Formatted_Creak/' + sys.argv[2]
        format_files(sys.argv[3], segAddress, creakAddress, outAddress)
    elif sys.argv[1] == 'reaper':
        if not 'COSPRO_0' in sys.argv[2]:
            if not 'Child' in sys.argv[2]:
                print(sys.argv[2])
                raise ValueError("Wrong input.")
        segAddress = refdirectory + '/2-Formatted_Segments/' + sys.argv[2]
        print(segAddress)
        reapAddress = refdirectory + '/1-Raw_Reaper_Results/' + sys.argv[2]
        outAddress = refdirectory + '/2-Formatted_Reaper_Results/' + sys.argv[2]
        format_files(sys.argv[3], segAddress, reapAddress, outAddress)
    else:
        format_files(sys.argv[4], sys.argv[1], sys.argv[2], sys.argv[3])
