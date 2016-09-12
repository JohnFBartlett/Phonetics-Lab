#!/usr/bin/python

import sys
import re
import os

def format_files(adjusted, breakfile, creakfile, reaperfile, measurements, out):
    # initialize formatted file
    # get part after slash
    pieces = adjusted.split('/')
    name = pieces[-1]
    # remove adjusted extension
    name = name[:-9]

    # .t2 is the extension of files formatted for task 2
    fileTitle = out + name + '.t2'
    # print "fileTitle is " + fileTitle
    out = open(fileTitle, 'w')

    # analyze title to get speech style, speaker ID
    # format COSPRO_(corpusNum)_(sid)(style/type)(fileno).(extension)
    [ignore, corpusNum, rest] = name.split('_')
    # get sid
    sid = re.sub(r'(.*)phr.*', r'\1', rest)
    # combine corpus number before speaker id for clarity
    sid = corpusNum + sid

    # get speech style
    style = get_speech_style(rest)

    # open .adjusted, .break, and .measurements files for this title
    with open(adjusted, 'r') as a:
        # open files if they exist
        if breakfile == 'N/A':
            b = 0
        else:
            b = open(breakfile, 'r')
        if creakfile == 'N/A':
            c = 0
        else:
            c = open(creakfile, 'r')
        if reaperfile == 'N/A':
            c = 0
        else:
            c = open(reaperfile, 'r')
        if measurements == 'N/A':
            c = 0
        else:
            c = open(measurements, 'r')

        # Go through formatting steps
        # 0. Write header lines
        out.write('Filename' + '\t' + 'Segment' + '\t' + 'Vowel?' + '\t' + 'Start Time(ms)' + '\t')
        out.write('End Time(ms)' + '\t' + 'Speaker ID' + '\t' + 'Speech Style' + '\t' + 'Preceding Seg. Break' + '\t')
        out.write('Current Seg. Break ' + '\t' + 'Current End Break ' + '\t')
        out.write('Preceding Segment ' + '\t' + 'Next Segment' + '\t' + next(m))
        
        # 1. Skip 2 header lines of break
        next(b)
        next(b)
        [bStart, bEnd, bItem] = next(b).split(' ')
         
        # 2. Try to skip first two line of .adjusted, read next two lines (if possible) and store them as 
        # [prevStart, prevEnd, prevSegment] and [currStart, currEnd, currSegment]
        try:
            next(a)
            next(a)
            [prevStart, prevEnd, prevSegment] = next(a).split(' ')
            [currStart, currEnd, currSegment] = next(a).split(' ')
        except IOError:
            print("File has fewer than two lines of content (besides header lines).\n")
            print("It is probably either the wrong type of file or was created incorrectly.\n")
        
        # variable first marks first iteration
        first = 1
        # for each line, do:
        for line in a:
            #read next .adjusted line as [nextStart, nextEnd, nextSegment]
            [nextStart, nextEnd, nextSegment] = line.split(' ')
            # 1. write filename
            # clear newline character
            name = re.sub(r'(.*)\n', r'\1', name)
            out.write(name + '\t')
            
            # 2. write currSegment, vowel and times
            # clear newline character
            currSegment = re.sub(r'(.*)\n', r'\1', currSegment)
            # detect vowels (Full list of vowels in SAMPA-T label method on p. 11
            # of Taiwan Mandarin Running Speech databases.pdf in documentation.)
            vowel = 'C'
            for letter in currSegment:
                if letter in 'iuyaEo?@U~}':
                    vowel = 'V'
            if 'n^' in currSegment:
                vowel = 'V'
            elif 'm^' in currSegment:
                vowel = 'V'
            elif 'sil' in currSegment:
                vowel = 'N/A'
            out.write(currSegment + '\t' + vowel + '\t' + currStart + '\t' + currEnd + '\t')
         
            # 3. print Speaker ID and speech style (acquired at beginning)
            # clear newline character
            sid = re.sub(r'(.*)\n', r'\1', sid)
            out.write(sid + '\t')
            out.write(style + '\t')
            
            # 4. print break at beginning of previous segment (N/A) if none
            while float(bEnd) < float(prevStart):
                # print "bEnd is " + bEnd + "and currEnd is " + currEnd
                try:
                    [bStart, bEnd, bItem] = next(b).split(' ')
                except:
                    # print "out"
                    out.write('N/A' + '\t')
                    break
            if float(prevStart) >= float(bStart) and float(prevStart) <= float(bEnd):
                # clear newline character
                # print "Break item before  is " + bItem
                bItem = re.sub(r'(.*)\n', r'\1', bItem)
                # print "Break item after  is " + bItem
                out.write(bItem + '\t')
            else:
                out.write('N/A' + '\t')
         
            # 5. print current .break section at beginning of segment (N/A) if none
            while float(bEnd) < float(currStart):
                # print "bEnd is " + bEnd + "and currEnd is " + currEnd
                try:
                    [bStart, bEnd, bItem] = next(b).split(' ')
                except:
                    # print "out"
                    out.write('N/A' + '\t')
                    break
            if float(currStart) >= float(bStart) and float(currStart) <= float(bEnd):
                # clear newline character
                bItem = re.sub(r'(.*)\n', r'\1', bItem)
                out.write(bItem + '\t')
            else:
                out.write('N/A' + '\t')
                # 6. print current .break section at end of segment (N/A) if none
            while float(bEnd) < float(currEnd):
                # print "bEnd is " + bEnd + "and currEnd is " + currEnd
                try:
                    [bStart, bEnd, bItem] = next(b).split(' ')
                except:
                    out.write('N/A' + '\t')
                    break
            if float(currEnd) >= float(bStart) and float(currEnd) <= float(bEnd):
                # clear newline character
                bItem = re.sub(r'(.*)\n', r'\1', bItem)
                out.write(bItem + '\t')
            else:
                out.write('N/A' + '\t')
        
        
                            # 7. print prevSegment -- say N/A for first segment
                            if first:
                                out.write('N/A' + '\t')
                                first = 0
                            else:
                                # clear newline character
                                prevSegment = re.sub(r'(.*)\n', r'\1', prevSegment)
                                out.write(prevSegment + '\t')
                                
                            # 8. write nextSegment
                            # clear newline character
                            nextSegment = re.sub(r'(.*)\n', r'\1', nextSegment)
                            out.write(nextSegment + '\t')
        
                            # 9. write creak datum
                            [cStart, cEnd, creakValue] = next(c)
                            out.write(creakValue + '\t')
        
                            # 10. write reaper .f0 and .pm
                            
                            
                            # 11. write one line of measurements 
                            try:
                                mLine = next(m)
                            except:
                                print "measurement file finished"
                                print "currStart " + currStart + " and currEnd " + currEnd
                            # clear newline character
                            mLine = re.sub(r'(.*)\n', r'\1', mLine)
                            out.write(mLine + '\n')

                            # 12. update time interval
                            # set [currStart, currEnd, currSegment] = [nextStart, nextEnd, nextSegment]
                            # set [prevStart, prevEnd, prevSegment] = [currStart, currEnd, currSegment]
                            [currStart, currEnd, currSegment] = [nextStart, nextEnd, nextSegment]
                            [prevStart, prevEnd, prevSegment] = [currStart, currEnd, currSegment]
                               
        
                        # after for loop print last line of info (looking ahead each iteration so this isn't included in loop)
                        # clear newline character
                        name = re.sub(r'(.*)\n', r'\1', name)
                        out.write(name + '\t')
        
                        # 2. write currSegment (maybe times later if Jianjing wants)
                        # clear newline character
                        currSegment = re.sub(r'(.*)\n', r'\1', currSegment)
                        out.write(currSegment + '\t')
                        
                        # 3. print Speaker ID and speech style (acquired at beginning)
                        # clear newline character
                        sid = re.sub(r'(.*)\n', r'\1', sid)
                        out.write(sid + '\t')
                        out.write(style + '\t')
        
                        # 4. print break at beginning of previous segment (N/A) if none
                        while bEnd < prevStart:
                            # print "bEnd is " + bEnd + "and currEnd is " + currEnd
                            try:
                                [bStart, bEnd, bItem] = next(b).split(' ')
                            except:
                                # print "out"
                                out.write('N/A' + '\t')
                                break
                        if prevStart >= bStart and prevStart <= bEnd:
                            # clear newline character
                            bItem = re.sub(r'(.*)\n', r'\1', bItem)
                            out.write(bItem + '\t')
                        else:
                            out.write('N/A' + '\t')
        
                        # 5. print current .break section at beginning of segment (N/A) if none
                        while bEnd < currStart:
                            # print "bEnd is " + bEnd + "and currEnd is " + currEnd
                            try:
                                [bStart, bEnd, bItem] = next(b).split(' ')
                            except:
                                # print "out"
                                out.write('N/A' + '\t')
                                break
                        if currStart >= bStart and currStart <= bEnd:
                            # clear newline character
                            bItem = re.sub(r'(.*)\n', r'\1', bItem)
                            out.write(bItem + '\t')
                        else:
                            out.write('N/A' + '\t')
        
                        # 6. print current .break section at end of segment (N/A) if none
                        while bEnd < currEnd:
                            # print "bEnd is " + bEnd + "and currEnd is " + currEnd
                            try:
                                [bStart, bEnd, bItem] = next(b).split(' ')
                            except:
                                # print "out"
                                out.write('N/A' + '\t')
                                break
                        if currEnd >= bStart and currEnd <= bEnd:
                            # clear newline character
                            bItem = re.sub(r'(.*)\n', r'\1', bItem)
                            out.write(bItem + '\t')
                        else:
                            out.write('N/A' + '\t')
                        
                        # 7. print prevSegment -- say N/A for first segment
                        if first:
                            out.write('N/A' + '\t')
                        else:
                            # clear newline character
                            prevSegment = re.sub(r'(.*)\n', r'\1', prevSegment)
                            out.write(prevSegment + '\t')
                
                        # write N/A for next segment since it's the last
                        out.write('N/A' + '\t')
                


                        # 11. write one line of measurements 
                        mLine = next(m)
                        # clear newline character
                        mLine = re.sub(r'(.*)\n', r'\1', mLine)
                        out.write(mLine + '\n')
                        
    out.close()
    # print "File has " + str(lineCount) + "lines\n"

def get_speech_style(pattern):
    if re.match(r'prg\d{3,4}sf', rest):
        return "Speaker Focus paragraph"
    elif re.match(r'prg\d{3,4}af1', rest):
        return = "Designed Focus(1) paragraph"
    elif re.match(r'prg\d{3,4}af2', rest):
        return = "Designed Focus(2) paragraph"
    elif re.match(r'prg\d{3,4}af3', rest):
        return = "Designed Focus(3) paragraph"
    elif re.match(r'prg\d{3,4}_df', rest):
        return = "Default focus paragraph"
    elif re.match(r'prg\d{3,4}', rest):
        return = "Speech paragraph"
    elif re.match(r'sptn\d{3,4}read', rest):
        return = "Spontaneous vs. read speech"
    elif re.match(r'sptn\d{3,4}', rest):
        return = "Spontaneous speech"
    elif re.match(r'phr\d{3,4}_d', rest):
        return = "Declarative sentence"
    elif re.match(r'phr\d{3,4}_i', rest):
        return = "Interrogative sentence"
    elif re.match(r'phr\d{3,4}_e', rest):
        return = "Exclamatory sentence"
    elif re.match(r'phr\d{3,4}_c', rest):
        return = "Carrier sentence"
    elif re.match(r'phr\d{3,4}_wd/np', rest):
        return = "Word salad without punctuation"
    elif re.match(r'phr\d{3,4}_wd/p', rest):
        return = "Word salad with punctuation"
    elif re.match(r'phr\d{3,4}_C', rest):
        return = "Phrase China corpus"
    elif re.match(r'phr\d{3,4}_T', rest):
        return = "Phrase Taiwan corpus"
    elif re.match(r'.*phr\d{3,4}', rest):
        return = "Utterance or phrase"
    else:
        print("Couldn't match style!")
        return = "Not found"

    # there will always be 7 arguments because apply_task2_formatting.py is the pipeline
    format_files(sys.argv[1], sys.argv[2], sys.argv[3], sys.argv[4], sys.argv[5], sys.argv[6])
