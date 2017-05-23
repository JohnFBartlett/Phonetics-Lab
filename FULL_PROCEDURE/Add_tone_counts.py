#!/usr/bin/python

import sys
import re

def count_tones(f, out):

    # this variable keeps track of the most recent timestamp printed
    # in the out file so it doesn't print the same time twice in a row
    # (rounding can sometimes lead to this problem)
    print f
    # Make sure file is correct type
    if not '.adjusted' in f:
        print 'Incorrect file type. Should be .adjusted'
    else: 

        T1_count = 0
        T2_count = 0
        T3_count = 0
        T4_count = 0
        T5_count = 0
        T2T3_count = 0
        T3T3_count = 0
    

        for i in os.listdir(os.getcwd()):
            if i.endswith(".asm") or i.endswith(".py"):
                ##print i
                continue
            else:
                continue


        # count all types of tones and the two combination types
        with open(f) as file:
            # skip first line (header line)
            next(file)
            [startTime, endTime, segment] = line.split(' ')
            
            # go through each line and add to proper sum
            if "1" in segment:
                T1_count += 1
                prev = 1
            elif "2" in segment:
                T2_count += 1
                prev = 2
            elif "3" in segment:
                T3_count += 1
                
                # also check for combination
                if prev == 3:
                    T3T3_count += 1
                elif prev == 2:
                    T2T3_count += 1
                prev = 3
            elif "4" in segment:
                T4_count += 1
                prev = 4
            elif "5" in segment:
                T5_count += 1
                prev = 5    
            # continue to next line
                
        # # THINK OF HOW TO GET PROPER TITLE
        # pieces = f.split('/')
        # title = pieces[-1]
        # title = re.sub(".adjusted", "", "")
        # fileTitle = out + title + '.tones'
        # print "fileTitle is " + fileTitle
        # out = open(fileTitle, 'w')
    
        # write results to outfile
        result1 = "T1_count = " + str(T1_count) + "\n"
        result2 = "T2_count = " + str(T2_count) + "\n"
        result3 = "T3_count = " + str(T3_count) + "\n"
        result4 = "T4_count = " + str(T4_count) + "\n"
        result5 = "T5_count = " + str(T5_count) + "\n"
        result6 = "T2T3_count = " + str(T2T3_count) + "\n"
        result7 = "T3T3_count = " + str(T3T3_count) + "\n"

        out.write("Tone Count for file " + f)
        out.write(result1)
        out.write(result2)
        out.write(result3)
        out.write(result4)
        out.write(result5)
        out.write(result6)
        out.write(result7)

        out.close()
        # print "File has " + str(lineCount) + " lines\n"

count_tones(sys.argv[1], sys.argv[2])