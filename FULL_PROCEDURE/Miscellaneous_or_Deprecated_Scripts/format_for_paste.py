#!/usr/bin/python

import sys

def prepare_for_paste(f, out):

    # this variable keeps track of the most recent timestamp printed
    # in the out file so it doesn't print the same time twoce in a row
    # (rounding can sometimes lead to this problem)
    print f
    prevTime = -1.00

    # initialize formatted file
    pieces = f.split('/')
    n = pieces[-1]
    fileTitle = out + n + '_f'
    # print "fileTitle is " + fileTitle
    out = open(fileTitle, 'w')

    # check which type of file it is
    if '.creak' in f:
        # it's a creak file
        # get filename for writing
        name = n[:-6]
        
        lineCount = 0
        with open(f) as file:
            # skip first line
            next(file)
            for line in file:
                # reprint with tab separation
                [time, state] = line.split(',')
                if time != prevTime:
                    out.write(name + '\t' + time + '\t' + state + '\n')
                    lineCount += 1
                    prevTime = time
        out.close()
        # print "File has " + str(lineCount) + "lines\n"
        
    elif '.break' in f:
        # it's a break file
        lineCount = 0
        with open(f) as file:
            # skip first two lines
            next(file)
            next(file)
            for line in file:
                [startTime, endTime, state] = line.split(' ')

                #print state every 10 milliseconds in interval
                for i in xrange(int(float(startTime)), int(float(endTime)), 10):
                    # round and convert to seconds
                    converted = float(int(i)/10)/100
                    if converted != prevTime:
                        out.write(str(converted) + '\t' + state + '\n')
                        lineCount += 1
                        prevTime = converted
        out.close()
        # print "File has " + str(lineCount) + "lines\n"

    elif '.adjusted' in f:
        # it's a segment file
        lineCount = 0
        with open(f) as file:
            # skip first two lines
            next(file)
            next(file)
            for line in file:
                [startTime, endTime, state] = line.split(' ')
                
                #print state every 10 milliseconds in interval
                for i in xrange(int(float(startTime)), int(float(endTime)), 10):
                    # round and convert to seconds
                    converted = float(int(i)/10)/100
                    if converted != prevTime:
                        out.write(str(converted) + '\t' + state + '\n')
                        lineCount += 1
                        prevTime = converted
        out.close()
        # print "File has " + str(lineCount) + " lines\n"

    elif '.f0' in f:
        # it's a pitch file
        lineCount = 0
        with open(f) as file:
            # skip first 7 lines
            next(file)
            next(file)
            next(file)
            next(file)
            next(file)
            next(file)
            next(file)
            for line in file:
                [time, ignore, pitch] = line.split(' ')

                # cut off extra digits
                time = float(int(float(time)*100))/100
                
                # print time and pitch
                if time != prevTime:
                    out.write(str(time) + '\t' + pitch + '\n')
                    lineCount += 1
                    prevTime = time
        out.close()
        # print "File has " + str(lineCount) + "lines\n"

    else:
        print 'Incorrect file type.'    

prepare_for_paste(sys.argv[1], sys.argv[2])