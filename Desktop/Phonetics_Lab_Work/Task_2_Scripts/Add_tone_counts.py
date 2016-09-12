#!/usr/bin/python

import sys
import re
import os

def count_tones(directory, out):
    
    T1_count = 0
    T2_count = 0
    T3_count = 0
    T4_count = 0
    T5_count = 0
    T2T3_count = 0
    T3T3_count = 0
    
    f = ""
    for f in os.listdir(directory):
        if f.endswith(".tones"): 
            print f
            # count all types of tones and the two combination types
            file = open(f, 'r')
            # skip first line (header line)
            next(file)
            
            # get T1 count for this file
            line = next(file)
            [t1, equals, count] = line.split(' ')

            # check formatting
            if "T1_count" != t1:
                print "T1 line not found. file incorrectly formatted."
                break
            else:
                T1_count += int(count)
            

            # get T2 count for this file
            line = next(file)
            [t2, equals, count] = line.split(' ')

            # check formatting
            if "T2_count" != t2:
                print "T2 line not found. file incorrectly formatted."
                break
            else:
                T2_count += int(count)


            # get T3 count for this file
            line = next(file)
            [t3, equals, count] = line.split(' ')

            # check formatting
            if "T3_count" != t3:
                print "T3 line not found. file incorrectly formatted."
                break
            else:
                T3_count += int(count)


            # get T4 count for this file
            line = next(file)
            [t4, equals, count] = line.split(' ')

            # check formatting
            if "T4_count" != t4:
                print "T4 line not found. file incorrectly formatted."
                break
            else:
                T4_count += int(count)


            # get T5 count for this file
            line = next(file)
            [t5, equals, count] = line.split(' ')

            # check formatting
            if "T5_count" != t5:
                print "T5 line not found. file incorrectly formatted."
                break
            else:
                T5_count += int(count)


            # get T2T3 count for this file
            line = next(file)
            [t2t3, equals, count] = line.split(' ')

            # check formatting
            if "T2T3_count" != t2t3:
                print "T2T3 line not found. file incorrectly formatted."
                break
            else:
                T2T3_count += int(count)


            # get T3T3 count for this file
            line = next(file)
            [t3t3, equals, count] = line.split(' ')

            # check formatting
            if "T3T3_count" != t3t3:
                print "T3T3 line not found. file incorrectly formatted."
                break
            else:
                T3T3_count += int(count)

            #close file
            file.close()
        else:
            print "file does not have .tones extension. Skipping..."
            continue

        
                
    # # THINK OF HOW TO GET PROPER TITLE
    # if all files are the same speaker
    # print "f = " + f
    # titlePiece = re.sub(r'(.*phr)\d{3}tones', '\1', f)
    # print titlePiece
    titlePiece = f[:-9]
    outtitle = titlePiece + "TOTAL.tones"
    print "outtitle is " + outtitle
    out = open(outtitle, 'w')
    
    # write results to outfile
    result1 = "T1_count = " + str(T1_count) + "\n"
    result2 = "T2_count = " + str(T2_count) + "\n"
    result3 = "T3_count = " + str(T3_count) + "\n"
    result4 = "T4_count = " + str(T4_count) + "\n"
    result5 = "T5_count = " + str(T5_count) + "\n"
    result6 = "T2T3_count = " + str(T2T3_count) + "\n"
    result7 = "T3T3_count = " + str(T3T3_count) + "\n"

    out.write("Total tone count for Tone Count for " + titlePiece)
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