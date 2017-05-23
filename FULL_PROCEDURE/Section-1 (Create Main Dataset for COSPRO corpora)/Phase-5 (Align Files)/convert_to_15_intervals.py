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
                        print("Does not match " + currName)
                        print("Skipping adjusted file "  + name)
                        break
                    # otherwise go to the next .creak file instead
                    else:
                        print("Does not match " + name)
                        print("Skipping .creak file." + currName)
                        currFile = otherFile + next(dircycle)
                        currName = re.sub(r'.*/(.*)', r'\1', currFile[:-6])
                else:
                    print("Name " + name + " matches creakName " + currName)
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
                                print(currStart)
                                print("milltime is " + str(milltime))
                                print("segment line is " + currStart + ", " + currEnd + ", " + currSegment + '\n')
    
                                try:
                                    cline = next(c)
                                    print("new line is " + cline)
                                except:
                                    print("No more lines left in creak file.")
                                    break

                                [time, creak] = cline.split(',')
                                # convert time to milliseconds
                                milltime = 1000*float(time)
    
                            # gather all measurement lines that are within segment range
                            while milltime >= float(currStart) and milltime <= float(currEnd):
                                # print "file " + name
                                # print str(milltime) + " is between currStart: " + currStart + " and currEnd: " + currEnd
                                lines.append([milltime, float(creak)])
                                counter += 1
    
                                try:
                                    cline = next(c)
                                except:
                                    print("No more lines left in creak file.")
                                    break

                                [time, creak] = cline.split(',')
                                # convert time to milliseconds
                                milltime = 1000*float(time)
    
                            # average creak value
                            # print time range, 
                            if counter != 0:
                                justvals = [elem[1] for elem in lines]
                                # print str(justvals)
                                avgline = float(sum(justvals) / float(counter))
                                # assign creak_vals 1-15
                                # - make an iterator for the available lines
                                lns = iter(lines)
                                [curr_time, curr_creak] = next(lns)
                                no_more = False
                                try:
                                    [next_time, next_creak] = next(lns)
                                except StopIteration:
                                    # this is the case when only 1 creak is within the seg interval
                                    # so, this creak should be printed for all 15 intervals
                                    no_more = True
                                if no_more:
                                    creak_vals = [curr_creak] * 15
                                else:
                                    # - for each interval, see which line is closest
                                    creak_vals = []
                                    interval = (float(currEnd) - float(currStart))/15.0
                                    # print "Number of justvals is " + str(len(justvals))
                                    for i in range(15):
                                        if no_more:
                                            creak_vals.append(next_creak)
                                        else:
                                            comp = (float(i) * interval) + float(currStart)
                                            while next_time < comp:
                                                if no_more:
                                                    break
                                                try:
                                                    [curr_time, curr_creak] = [next_time, next_creak]
                                                    [next_time, next_creak] = next(lns)
                                                except StopIteration:
                                                    # there are no more items in lns, so the rest should be next_creak
                                                    no_more = True
                                            # see which creak time is closest
                                            currdiff = abs(comp - curr_time)
                                            nextdiff = abs(comp - next_time)
                                            if currdiff < nextdiff:
                                                # print "Currdiff " + str(currdiff) + " is less than Nextdiff " + str(nextdiff)
                                                # print "Curr, " + str(curr_time) + " is closer to " + str(comp) + " than " + str(next_time)
                                                creak_vals.append(curr_creak)
                                            else:
                                                # print "Nextdiff " + str(nextdiff) + " is less than Currdiff " + str(currdiff)
                                                # print "Next, " + str(next_time) + " is closer to " + str(comp) + " than " + str(curr_time)
                                                creak_vals.append(next_creak)
                                # print "Justvals is   " + str(justvals)
                                # print "creak_vals is " + str(creak_vals)
                                # print("=====================================")
                                # print("Writing Line: " + currStart + '\t' + currEnd + '\t' + str(avgline))
                                # print("Length of creak_vals is " + str(len(creak_vals)))
                                # print("=====================================")
                                out.write(currStart + '\t' + currEnd + '\t' + str(avgline) + '\t')
                                for i in range(15):
                                    out.write(str(creak_vals[i]))
                                    if i < 14:
                                        out.write('\t')
                                out.write('\n')
                            # if there are no creak lines within the range
                            # which would be if the segment interval is too small,
                            # just take the previous creak line -- it should be very close
                            else:
                                print("NO CREAK LINE BETWEEN INTERVAL, taking previous.")
                                print("=====================================")
                                print("Writing Line: " + currStart + '\t' + currEnd + '\t' + str(float(creak)))
                                print("=====================================")
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

                    print("Done with file " + name)
                    out.close()
        elif ".f0" in otherFiles[1]:
            print("Files are .f0")
            print(otherFiles)
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
                        print("Skipping adjusted file " + name)
                        print("Does not match " + currName)
                        break
                    # otherwise go to the next .creak file instead
                    else:
                        print("Skipping .f0 file " + currName)
                        print("Does not match " + name)
                        currFile = otherFile + next(dircycle)
                        currName = re.sub(r'.*/(.*)', r'\1', currFile[:-3])
                else:
                    print("Name " + name + " matches creakName " + currName)
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
                                    print("No more lines left in f0 file.")
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
                                    print("No more lines left in f0 file.")
                                    break

                                [time, pm, f0] = cline.split(' ')
                                # convert time to milliseconds
                                milltime = 1000*float(time)
                                # print milltime
    
                            # average creak value
                            # print time range, 
                            # print " counter is " + str(counter)
                            if counter != 0:
                                justf0vals = [elem[1] for elem in lines]
                                justpmvals = [elem[2] for elem in lines]
                                avgf0 = float(sum(justf0vals) / float(counter))
                                avgpm = float(sum(justpmvals) / float(counter))

                                # assign creak_vals 1-15
                                # - make an iterator for the available lines
                                lns = iter(lines)
                                [curr_time, curr_f0, curr_pm] = next(lns)
                                no_more = False
                                try:
                                    [next_time, next_f0, next_pm] = next(lns)
                                except StopIteration:
                                    # this is the case when only 1 creak is within the seg interval
                                    # so, these values should be printed for all 15 intervals
                                    # print "Just one line " + str([curr_time, curr_f0, curr_pm])
                                    no_more = True
                                if no_more:
                                    f0_vals = [curr_f0] * 15
                                    pm_vals = [curr_pm] * 15
                                else:
                                    # - for each interval, see which line is closest
                                    f0_vals = []
                                    pm_vals = []
                                    interval = (float(currEnd) - float(currStart))/15.0
                                    # print "Number of justvals is " + str(len(justvals))
                                    for i in range(15):
                                        if no_more:
                                            f0_vals.append(next_f0)
                                            pm_vals.append(next_pm)
                                        else:
                                            comp = (float(i) * interval) + float(currStart)
                                            while next_time < comp:
                                                if no_more:
                                                    break
                                                try:
                                                    [curr_time, curr_f0, curr_pm] = [next_time, next_f0, next_pm]
                                                    [next_time, next_f0, next_pm] = next(lns)
                                                except StopIteration:
                                                    # there are no more items in lns, so the rest should be next_
                                                    no_more = True
                                            # see which time is closest
                                            currdiff = abs(comp - curr_time)
                                            nextdiff = abs(comp - next_time)
                                            if currdiff < nextdiff:
                                                # print "Currdiff " + str(currdiff) + " is less than Nextdiff " + str(nextdiff)
                                                # print "Curr, " + str(curr_time) + " is closer to " + str(comp) + " than " + str(next_time)
                                                f0_vals.append(curr_f0)
                                                pm_vals.append(curr_pm)
                                            else:
                                                # print "Nextdiff " + str(nextdiff) + " is less than Currdiff " + str(currdiff)
                                                # print "Next, " + str(next_time) + " is closer to " + str(comp) + " than " + str(curr_time)
                                                f0_vals.append(next_f0)
                                                pm_vals.append(next_pm)

                                # print "Justf0vals is   " + str(justf0vals)
                                # print "f0_vals is " + str(f0_vals)
                                # print("=====================================")
                                # print("Writing Line: " + currStart + '\t' + currEnd + '\t' + str(avgf0) + '\t' + str(avgpm))
                                # # print("Length of f0_vals is " + str(len(f0_vals)))
                                # print("=====================================")

                                out.write(currStart + '\t' + currEnd + '\t' + str(avgf0) + '\t')
                                for i in range(15):
                                    out.write(str(f0_vals[i]) + '\t')
                                out.write(str(avgpm) + '\t')
                                for i in range(15):
                                    out.write(str(pm_vals[i]))
                                    if i < 14:
                                        out.write('\t')
                                out.write('\n')
    
                            else:
                                print("NO CREAK LINE BETWEEN INTERVAL, taking previous.")
                                print("=====================================")
                                print("Writing Line: " + currStart + '\t' + currEnd + '\t' + str(float(f0)) + '\t' + str(float(pm)))
                                print("=====================================")
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

                    print("Done with file " + name)
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
    print("comparing")
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
        print("Failed COSPRO comparison")
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
        print("Failed COSPRO comparison")
        return False
    # print(adjspeakId + ',' + adjfiletype + ',' + adjnum)
    # print(mspeakId + ',' + mfiletype + ',' + mnum)

    # see if they are the same gender
    if adjgender in mgender:
        print('check1 gender is same')
        # see if they are the same speaker
        if int(adjspeakId) == int(mspeakId):
            print('check2 is same')
            # see if they are the same filetype (phr vs. w vs. prg.)
            if adjfiletype in mfiletype:
                print('check3 type is same')
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

# sample command python ~/Desktop/Phonetics_Lab_Work/Task_2_Scripts/convert_to_15_intervals.py creak COSPRO_01/ 10
refdirectory = dirname('/Users/John/Desktop/COSPRO_DATA_BIN/Task2_Formatting/')
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
