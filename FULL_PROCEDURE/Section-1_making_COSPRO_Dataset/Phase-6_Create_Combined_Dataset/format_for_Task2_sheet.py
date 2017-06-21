#!/usr/bin/python2.6

import sys
import re
import os

def format_files(adjusted, breakfile, creakfile, reaperfile, measurements, out):
    # Check if from Childrens Data
    childrens = False
    if 'Child' in out:
        childrens = True

    pieces = adjusted.split('/')
    name = pieces[-1]
    # remove adjusted_fixed extension
    if 'phn' in name:
        name = name[:-10]
    else:
        name = name[:-15]

    # .t2 is the extension of files formatted for task 2
    fileTitle = out + name + '.t2.txt'
    # print "fileTitle is " + fileTitle
    out = open(fileTitle, 'w')

    style = ""
    sid = ""
    if childrens:
        # assign speech style, speaker ID
        # sample file: c_f_svo_a10_s2_p06_t135_svo_r1.f0
        # sid would be a10s2p06
        style = "Utterance or Phrase"
        sid = re.sub(r'.*_(a[\d\w]{1,2})_(s\d)_(p\d+)_.*', r'\1\2\3', name)
    else:
        # analyze title to get speech style, speaker ID
        # format COSPRO_(corpusNum)_(sid)(style/type)(fileno).(extension)
        title = name.split('_')
        if len(title) == 4:
            rest = title[2] + title[3]
            corpusNum = title[1]
        else:
            [ignore, corpusNum, rest] = title
        # get sid
        sid = re.sub(r'(.*)phr.*', r'\1', rest)
        # combine corpus number before speaker id for clarity
        sid = corpusNum + sid
        # get speech style
        style = get_speech_style(rest)


    # open .adjusted, .break, and .measurements files for this title
    # print "Current directory is " + os.getcwd()
    # getting relative path for each inputted file
    arel = os.path.relpath(adjusted)
    brel = os.path.relpath(breakfile)
    crel = os.path.relpath(creakfile)
    rrel = os.path.relpath(reaperfile)
    mrel = os.path.relpath(measurements)

    ccount = 0
    bcount = 0
    rcount = 0
    mcount = 0
    scount = 0

    with open(arel, 'r') as a:
        # open files if they exist
        if breakfile == 'N/A':
            # print 'bad'
            b = 0
        else:
            b = open(brel, 'r')
            # print 'success!'
        if creakfile == 'N/A':
            c = 0
        else:
            c = open(crel, 'r')
        if reaperfile == 'N/A':
            r = 0
        else:
            r = open(rrel, 'r')
        if measurements == 'N/A':
            m = 0
        else:
            m = open(mrel, 'r')

        # Go through formatting steps
        # 0. Write header lines
        out.write('Filename' + '\t' 'Sentence No.' + '\t' + 'Segment' + '\t' + 'Tone' + '\t' + 'Next Seg Tone' + '\t' + 'Vowel?' + '\t' + 'Start Time(ms)' + '\t')
        out.write('End Time(ms)' + '\t' + 'Speaker ID' + '\t' + 'Speech Style' + '\t' + 'Preceding Seg. Break' + '\t')
        out.write('Current Seg. Break ' + '\t' + 'Current End Break ' + '\t' + 'Preceding Segment ' + '\t' + 'Next Segment' + '\t')
        out.write('Creak_mean' + '\t' + 'Creak_mean001' + '\t' + 'Creak_mean002' + '\t' + 'Creak_mean003' + '\t' + 'Creak_mean004' + '\t')
        out.write('Creak_mean005' + '\t' + 'Creak_mean006' + '\t' + 'Creak_mean007' + '\t' + 'Creak_mean008' + '\t' + 'Creak_mean009' + '\t')
        out.write('Creak_mean010' + '\t' + 'Creak_mean011' + '\t' + 'Creak_mean012' + '\t' + 'Creak_mean013' + '\t' + 'Creak_mean014' + '\t')
        out.write('Creak_mean015' + '\t' + 'f0_mean' + '\t' + 'f0_mean001' + '\t' + 'f0_mean002' + '\t' + 'f0_mean003' + '\t')
        out.write('f0_mean004' + '\t' + 'f0_mean005' + '\t' + 'f0_mean006' + '\t' + 'f0_mean007' + '\t' + 'f0_mean008' + '\t' + 'f0_mean009' + '\t')
        out.write('f0_mean010' + '\t' + 'f0_mean011' + '\t' + 'f0_mean012' + '\t' + 'f0_mean013' + '\t' + 'f0_mean014' + '\t' + 'f0_mean015' + '\t')
        out.write('Pitchmark_mean' + '\t' + 'Pitchmark_mean001' + '\t' + 'Pitchmark_mean002' + '\t' + 'Pitchmark_mean003' + '\t' + 'Pitchmark_mean004' + '\t')
        out.write('Pitchmark_mean005' + '\t' + 'Pitchmark_mean006' + '\t' + 'Pitchmark_mean007' + '\t' + 'Pitchmark_mean008' + '\t' + 'Pitchmark_mean009' + '\t')
        out.write('Pitchmark_mean010' + '\t' + 'Pitchmark_mean011' + '\t' + 'Pitchmark_mean012' + '\t' + 'Pitchmark_mean013' + '\t')
        out.write('Pitchmark_mean014' + '\t' + 'Pitchmark_mean015' + '\t')
        if m:
            out.write(str(next(m)))
        else:
            out.write("Measurements" + '\n')
        
        # 1. Skip 2 header lines of break
        if b:
            next(b)
            next(b)
            pieces = re.split(' ', next(b))
            if len(pieces) > 2:
                bStart = pieces[0]
                bEnd = pieces[1]
                bItem = pieces[2]
            bcount += 1
            # print "Break line " + str(bcount)
         
        # 2. Try to skip first two line of .adjusted, read next two lines (if possible) and store them as 
        # [prevStart, prevEnd, prevSegment] and [currStart, currEnd, currSegment]
        try:
            next(a)
            next(a)
            [currStart, currEnd, currSegment] = re.split(' |\t', next(a))
            scount += 1
            # print "Segment line " + str(scount)
        except IOError:
            print("File has fewer than two lines of content (besides header lines).\n")
            print("It is probably either the wrong type of file or was created incorrectly.\n")
        
        # variable first marks first iteration
        first = 1
        backlog1_S = ""
        backlog1_E = ""
        backlog1_I = ""
        backlog2_S = ""
        backlog2_E = ""
        backlog2_I = ""
        
        # =================== START OF LOOP =================================

        # for each line, do:
        for line in a:
            scount += 1
            # print "Segment line " + str(scount)
            #read next .adjusted line as [nextStart, nextEnd, nextSegment]
            try:
                # print "A line is " + line
                pieces = re.split(' |\t', line)
                if len(pieces) > 2:
                    nextStart = pieces[0]
                    nextEnd = pieces[1]
                    nextSegment = pieces[2]
            except ValueError:
                print(line)
                raise ValueError("Line 130, line can't be split correctly")
        
            # 1. write filename and sentence number
            # clear newline character
            name = re.sub(r'(.*)\n', r'\1', name)
            out.write(name + '\t')

            senNum = re.sub(r'.*(\d+)$', r'\1', name)
            out.write(senNum + '\t')
                            
            # 2. write currSegment, vowel and times
            # clear newline character
            currSegment = re.sub(r'(.*)\n', r'\1', currSegment)
            out.write(currSegment + '\t')

            # get tone from currSegment, if possible
            tone = re.sub(r'.*(\d+).*', r'\1', currSegment)
            if currSegment == tone:
                # no tone found
                out.write('N/A' + '\t')
            else:
                out.write(tone + '\t')

            # get tone from nextSegment, if possible
            nextSegment = re.sub(r'(.*)\n', r'\1', nextSegment)
            tone = re.sub(r'.*(\d+).*', r'\1', nextSegment)
            if nextSegment == tone:
                # no tone found
                out.write('N/A' + '\t')
            else:
                out.write(tone + '\t')
        
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
        
            out.write(vowel + '\t' + currStart + '\t' + currEnd + '\t')
                        
        
            # 3. print Speaker ID and speech style (acquired at beginning)
            # clear newline character
            sid = re.sub(r'(.*)\n', r'\1', sid)
            out.write(sid + '\t')
            out.write(style + '\t')
                            
            # 4. print break at beginning of previous segment (N/A) if none
            if first:
                # print "first iteration"
                out.write('N/A' + '\t')
            else:
                written = 0
                if b:
                    # print "bEnd is " + bEnd + "and prevStart is " + prevStart
                    while float(bEnd) <= float(prevStart):
                        print "next 1"
                        # store previous break lines if needed
                        [backlog2_S, backlog2_E, backlog2_I] = [backlog1_S, backlog1_E, backlog1_I]
                        [backlog1_S, backlog1_E, backlog1_I] = [bStart, bEnd, bItem]
                        try:
                            pieces = re.split(' ', next(b))
                            if len(pieces) > 2:
                                bStart = pieces[0]
                                bEnd = pieces[1]
                                bItem = pieces[2]
                            bcount += 1
                            print "PREVVVVVV"
                            print bStart
                            print "Break line a " + str(bcount)
                        except StopIteration:
                            # print "out"
                            out.write('no more prev beg break data' + '\t')
                            written = 1
                            break
                    # print "[" + backlog1_S + "," + backlog1_E + "," + backlog1_I + "]"
                    if float(bStart) <= float(prevStart) and float(bEnd) >= float(prevStart):
                        # print "curr b0 worked"
                        # print "ba0: " + bStart + ", " + bEnd
                        # print "prevStart " + prevStart + " is between " + bStart + " and " + bEnd
                        # print "ba1: " + backlog1_S + ", " + backlog1_E
                        # print "ba2: " + backlog2_S + ", " + backlog2_E
                        # clear newline character
                        bItem = re.sub(r'(.*)\n', r'\1', bItem)
                        out.write(bItem + '\t')

                    # This condition is a special case:
                    # it only occurs if we are looking at the first line which does NOT
                    # start at 0. This would result in bstart being after currStart, but there 
                    # would be no backlog to refer to, since bStart is the first line of the 
                    # break file. In this case I will just print the current break anyway.
                    elif backlog1_S == "":
                        print("SPECIAL CASE: break file does not start at 0.")
                        bItem = re.sub(r'(.*)\n', r'\1', bItem)
                        out.write(bItem + '\t')

                    # check if line before is in range
                    elif float(backlog1_S) <= float(prevStart) and float(backlog1_E) >= float(prevStart):
                        # print "Backlog prev works!"
                        # print "ba0: " + bStart + ", " + bEnd + ", " + bItem
                        # print "ba1: " + backlog1_S + ", " + backlog1_E + ", " + backlog1_I
                        # print "ba2: " + backlog2_S + ", " + backlog2_E + ", " + backlog2_I
                        # clear newline character
                        backlog1_I = re.sub(r'(.*)\n', r'\1', backlog1_I)
                        out.write(backlog1_I + '\t')
                    # check if 2 lines before is in range
                    elif backlog2_S and float(backlog2_S) <= float(prevStart) and float(backlog2_E) >= float(prevStart):
                        # clear newline character
                        backlog2_I = re.sub(r'(.*)\n', r'\1', backlog2_I)
                        out.write(backlog2_I + '\t')
                    elif not written:
                        out.write('No item within range' + '\t')
                        # print "prevStart " + prevStart + " not within " + bStart + " and " + bEnd
                        # print "ba0: " + bStart + ", " + bEnd
                        # print "ba1: " + backlog1_S + ", " + backlog1_E
                        # print "ba2: " + backlog2_S + ", " + backlog2_E
                        written = 1
                else:
                        out.write('no data' + '\t')
        
            # 5. print current .break section at beginning of segment (N/A) if none
            written = 0
            if b:
                while float(bEnd) < float(currStart):
                    # print "bEnd is " + bEnd + "and currEnd is " + currEnd
                    # store previous break lines if needed
                    [backlog2_S, backlog2_E, backlog2_I] = [backlog1_S, backlog1_E, backlog1_I]
                    [backlog1_S, backlog1_E, backlog1_I] = [bStart, bEnd, bItem]
                    try:
                        pieces = re.split(' ', next(b))
                        if len(pieces) > 2:
                            bStart = pieces[0]
                            bEnd = pieces[1]
                            bItem = pieces[2]
                        bcount += 1
                        # print "CURRENT"
                        # print bStart
                        # print "Break line b " + str(bcount)
                    except StopIteration:
                        # print "out"
                        out.write('no more curr beg break data' + '\t')
                        written = 1
                        break
                # print "[" + backlog1_S + "," + backlog1_E + "," + backlog1_I + "]"
                # check if current line is in range
                if float(bStart) <= float(currStart) and float(bEnd) >= float(currStart):
                    # print "curr b0 worked"
                    # print "ba0: " + bStart + ", " + bEnd
                    # print "ba1: " + backlog1_S + ", " + backlog1_E
                    # print "ba2: " + backlog2_S + ", " + backlog2_E
                    # clear newline character
                    bItem = re.sub(r'(.*)\n', r'\1', bItem)
                    out.write(bItem + '\t')

                # This condition is a special case:
                # it only occurs if we are looking at the first line which does NOT
                # start at 0. This would result in bstart being after currStart, but there 
                # would be no backlog to refer to, since bStart is the first line of the 
                # break file. In this case I will just print the current break anyway.
                elif backlog1_S == "":
                    print "SPECIAL CASE: break file does not start at 0."
                    bItem = re.sub(r'(.*)\n', r'\1', bItem)
                    out.write(bItem + '\t')

                # check if line before is in range
                elif float(backlog1_S) <= float(currStart) and float(backlog1_E) >= float(currStart):
                    # print "curr b1 worked"
                    # print "ba0: " + bStart + ", " + bEnd
                    # print "ba1: " + backlog1_S + ", " + backlog1_E
                    # print "ba2: " + backlog2_S + ", " + backlog2_E
                    # clear newline character
                    backlog1_I = re.sub(r'(.*)\n', r'\1', backlog1_I)
                    out.write(backlog1_I + '\t')

                # check if 2 lines before is in range
                elif backlog2_S and float(backlog2_S) <= float(currStart) and float(backlog2_E) >= float(currStart):
                    # clear newline character
                    backlog2_I = re.sub(r'(.*)\n', r'\1', backlog2_I)
                    out.write(backlog2_I + '\t')
                elif not written:
                    out.write('No item within range' + '\t')
                    print "currStart " + currStart + " not within " + bStart + " and " + bEnd
                    # print "ba0: " + bStart + ", " + bEnd
                    # print "ba1: " + backlog1_S + ", " + backlog1_E
                    # print "ba2: " + backlog2_S + ", " + backlog2_E
                    written = 1
            else:
                    out.write('no data' + '\t')
        
            # 6. print current .break section at end of segment (N/A) if none
            written = 0
            if b:
                while float(bEnd) < float(currEnd):
                    # print "bEnd is " + bEnd + "and currEnd is " + currEnd
                    # print "next 3"
                    # store previous break lines if needed
                    if backlog1_S:
                        [backlog2_S, backlog2_E, backlog2_I] = [backlog1_S, backlog1_E, backlog1_I]
                    [backlog1_S, backlog1_E, backlog1_I] = [bStart, bEnd, bItem]
                    try:
                        pieces = re.split(' ', next(b))
                        if len(pieces) > 2:
                            bStart = pieces[0]
                            bEnd = pieces[1]
                            bItem = pieces[2]
                        bcount += 1
                        # print bStart
                        # print "Break line b " + str(bcount)
                    except ValueError:
                        print str(pieces)
                        raise ValueError("Line 332, line can't be split correctly")
                    except StopIteration:
                        out.write('no more curr end break data' + '\t')
                        written = 1
                        break
                if float(bStart) <= float(currEnd) and float(bEnd) >= float(currEnd):
                    # clear newline character
                    bItem = re.sub(r'(.*)\n', r'\1', bItem)
                    out.write(bItem + '\t')
                elif not written:
                    out.write('No item within range' + '\t')
                    # print "currEnd " + currEnd + " not within " + bStart + " and " + bEnd
                    # print "ba0: " + bStart + ", " + bEnd
                    # print "ba1: " + backlog1_S + ", " + backlog1_E
                    # print "ba2: " + backlog2_S + ", " + backlog2_E
                    written = 1
            else:
                out.write('no data' + '\t')
                written = 1
        
        
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
            written = 0
            if c:
                try:
                    creakdata = next(c).split('\t')
                    creakValues = creakdata[2:]
                    ccount += 1
                    # print "Creak line " + str(ccount)
                    # clear newline character
                    creakValues[-1] = re.sub(r'(.*)\n', r'\1', creakValues[-1])
                    for elem in creakValues:
                        out.write(elem + '\t')
                except StopIteration:
                    print "No more c lines"
                    out.write('no more creak data' + '\t')
                    written = 1
            else:
                out.write('no data' + '\t')
                written = 1
        
            # 10. write reaper .f0 and .pm
            written = 0
            if r:
                try:
                    reaperdata = next(r).split('\t')
                    reaperValues = reaperdata[2:]
                    rcount += 1
                    # print "Reaper line " + str(rcount)
                    # clear newline characters
                    reaperValues[-1] = re.sub(r'(.*)\n', r'\1', reaperValues[-1])
                    for elem in reaperValues:
                        out.write(elem + '\t')
                except StopIteration:
                    print "No more reaper lines"
                    out.write('no more reaper data' + '\t')
                    written = 1
            else:
                out.write('no data' + '\t')
                written = 1
                            
            # 11. write one line of measurements 
            written = 0
            if m:
                try:
                    mLine = next(m)
                    mcount += 1
                    # print("Meas line " + str(mcount))
                    # print("Line is " + mLine)
                    # clear newline character
                    mLine = re.sub(r'(.*)\n', r'\1', mLine)
                    out.write(mLine + '\n')
                except StopIteration:
                    print "measurement file finished"
                    print "currStart " + currStart + " and currEnd " + currEnd
                    out.write('no more measure data' + '\n')
                    written = 1
            else:
                out.write('no data' + '\n')
                written = 1

            # 12. update time interval
            # set [currStart, currEnd, currSegment] = [nextStart, nextEnd, nextSegment]
            # set [prevStart, prevEnd, prevSegment] = [currStart, currEnd, currSegment]
            [prevStart, prevEnd, prevSegment] = [currStart, currEnd, currSegment]
            [currStart, currEnd, currSegment] = [nextStart, nextEnd, nextSegment]

            # print "END ITER"

            # =================== END OF LOOP =================================
                               
        
        # after for loop print last line of info (looking ahead each iteration so this isn't included in loop)
        # clear newline character
        name = re.sub(r'(.*)\n', r'\1', name)
        out.write(name + '\t')
        
        # 2. get currSegment, vowel, times
        # clear newline character
        currSegment = re.sub(r'(.*)\n', r'\1', currSegment)
        out.write(currSegment + '\t')

        # get tone from currSegment, if possible
        tone = re.sub(r'.*(\d+).*', r'\1', currSegment)
        if currSegment == tone:
            # no tone found
            out.write('N/A' + '\t')
        else:
            out.write(tone + '\t')

        # This is the last line, so next Tone should always be N/A
        out.write('N/A' + '\t')

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
        
        # write currSegment, vowel, times
        out.write(vowel + '\t' + currStart + '\t' + currEnd + '\t')
                        
        # 3. print Speaker ID and speech style (acquired at beginning)
        # clear newline character
        sid = re.sub(r'(.*)\n', r'\1', sid)
        out.write(sid + '\t')
        out.write(style + '\t')
        
        # 4. print break at beginning of previous segment (N/A) if none
        if first:
                print "first iteration"
                out.write('N/A' + '\t')
        else:
            written = 0
            if b:
                while float(bEnd) < float(prevStart):
                    # print "bEnd is " + bEnd + "and currEnd is " + currEnd
                    [backlog2_S, backlog2_E, backlog2_I] = [backlog1_S, backlog1_E, backlog1_I]
                    [backlog1_S, backlog1_E, backlog1_I] = [bStart, bEnd, bItem]
                    try:
                        pieces = re.split(' ', next(b))
                        if len(pieces) > 2:
                            bStart = pieces[0]
                            bEnd = pieces[1]
                            bItem = pieces[2]
                        bcount += 1
                        # print bStart
                        # print "Break line a " + str(bcount)
                    except StopIteration:
                        # print "out"
                        out.write('no more prev beg break data' + '\t')
                        written = 1
                        break
                if float(bStart) <= float(prevStart) and float(bEnd) >= float(prevStart):
                    # clear newline character
                    bItem = re.sub(r'(.*)\n', r'\1', bItem)
                    out.write(bItem + '\t')
                # check if line before is in range
                elif float(backlog1_S) <= float(prevStart) and float(backlog1_E) >= float(prevStart):
                    # clear newline character
                    backlog1_I = re.sub(r'(.*)\n', r'\1', backlog1_I)
                    out.write(backlog1_I + '\t')
                # check if 2 lines before is in range
                elif backlog2_S and float(backlog2_S) <= float(prevStart) and float(backlog2_E) >= float(prevStart):
                    # clear newline character
                    backlog2_I = re.sub(r'(.*)\n', r'\1', backlog2_I)
                    out.write(backlog2_I + '\t')
                elif not written:
                    out.write('No item within range' + '\t')
                    # print "prevStart " + prevStart + " not within " + bStart + " and " + bEnd
                    # print "ba0: " + bStart + ", " + bEnd
                    # print "ba1: " + backlog1_S + ", " + backlog1_E
                    # print "ba2: " + backlog2_S + ", " + backlog2_E
                    written = 1
            else:
                    out.write('no data' + '\t')
        
        # 5. print current .break section at beginning of segment (N/A) if none
        written = 0
        if b:
            while float(bEnd) < float(currStart):
                # print "bEnd is " + bEnd + "and currEnd is " + currEnd
                [backlog2_S, backlog2_E, backlog2_I] = [backlog1_S, backlog1_E, backlog1_I]
                [backlog1_S, backlog1_E, backlog1_I] = [bStart, bEnd, bItem]
                try:
                    pieces = re.split(' ', next(b))
                    if len(pieces) > 2:
                        bStart = pieces[0]
                        bEnd = pieces[1]
                        bItem = pieces[2]
                    bcount += 1
                    # print bStart
                    # print "Break line b " + str(bcount)
                except StopIteration:
                    # print "out"
                    out.write('no more curr beg break data' + '\t')
                    written = 1
                    break
            if float(bStart) <= float(currStart) and float(bEnd) >= float(currStart):
                # clear newline character
                bItem = re.sub(r'(.*)\n', r'\1', bItem)
                out.write(bItem + '\t')
            # check if line before is in range
            elif float(backlog1_S) <= float(currStart) and float(backlog1_E) >= float(currStart):
                # clear newline character
                backlog1_I = re.sub(r'(.*)\n', r'\1', backlog1_I)
                out.write(backlog1_I + '\t')
            # check if 2 lines before is in range
            elif backlog2_S and float(backlog2_S) <= float(currStart) and float(backlog2_E) >= float(currStart):
                # clear newline character
                backlog2_I = re.sub(r'(.*)\n', r'\1', backlog2_I)
                out.write(backlog2_I + '\t')
            elif not written:
                out.write('No item within range' + '\t')
                # print "currStart " + currStart + " not within " + bStart + " and " + bEnd
                # print "ba0: " + bStart + ", " + bEnd
                # print "ba1: " + backlog1_S + ", " + backlog1_E
                # print "ba2: " + backlog2_S + ", " + backlog2_E
                written = 1
        else:
                out.write('no data' + '\t')
        
        # 6. print current .break section at end of segment (N/A) if none
        written = 0
        if b:
            while float(bEnd) < float(currEnd):
                # print "bEnd is " + bEnd + "and currEnd is " + currEnd
                [backlog2_S, backlog2_E, backlog2_I] = [backlog1_S, backlog1_E, backlog1_I]
                [backlog1_S, backlog1_E, backlog1_I] = [bStart, bEnd, bItem]
                try:
                    pieces = re.split(' ', next(b))
                    if len(pieces) > 2:
                        bStart = pieces[0]
                        bEnd = pieces[1]
                        bItem = pieces[2]
                    bcount += 1
                    # print bStart
                    # print "Break line b " + str(bcount)
                except StopIteration:
                    out.write('no more curr end break data' + '\t')
                    written = 1
                    break
            if float(bStart) <= float(currEnd) and float(bEnd) >= float(currEnd):
                # clear newline character
                bItem = re.sub(r'(.*)\n', r'\1', bItem)
                out.write(bItem + '\t')
            elif not written:
                out.write('No item within range' + '\t')
                # print "currEnd " + currEnd + " not within " + bStart + " and " + bEnd
                # print "ba0: " + bStart + ", " + bEnd
                # print "ba1: " + backlog1_S + ", " + backlog1_E
                # print "ba2: " + backlog2_S + ", " + backlog2_E
                written = 1
        else:
            out.write('no data' + '\t')
            written = 1
                        
        # 7. print prevSegment -- say N/A for first segment
        if first:
            # this should never be the case
            out.write('N/A 5' + '\t')
        else:
            # clear newline character
            prevSegment = re.sub(r'(.*)\n', r'\1', prevSegment)
            out.write(prevSegment + '\t')
                
        # 8. write N/A for next segment since it's the last
        out.write('N/A next segment' + '\t')
                
        # 9. write creak datum
        if c:
            try:
                creakdata = next(c).split('\t')
                creakValues = creakdata[2:]
                ccount += 1
                # print "Creak line " + str(ccount)
                # clear newline character
                creakValues[-1] = re.sub(r'(.*)\n', r'\1', creakValues[-1])
                for elem in creakValues:
                    out.write(elem + '\t')
            except StopIteration:
                print "No more c lines"
                out.write('no more creak data' + '\t')
        else:
                out.write('no data' + '\t')
        
        # 10. write reaper .f0 and .pm
        if r:
            try:
                reaperdata = next(r).split('\t')
                reaperValues = reaperdata[2:]
                rcount += 1
                # print "Reaper line " + str(rcount)
                # clear newline characters
                reaperValues[-1] = re.sub(r'(.*)\n', r'\1', reaperValues[-1])
                for elem in reaperValues:
                    out.write(elem + '\t')
            except StopIteration:
                print "No more reaper lines"
                out.write('no more reaper data' + '\t')
        else:
                out.write('no data' + '\t')

        # 11. write one line of measurements 
        if m:
            try:
                mLine = next(m)
                mcount += 1
                # print("Meas line " + str(mcount))
                # clear newline character
                # print("Line is " + mLine)
                mLine = re.sub(r'(.*)\n', r'\1', mLine)
                out.write(mLine + '\n')
            except StopIteration:
                out.write('no more voicesauce data' + '\t')
                print("measurement file finished")
                print("currStart " + currStart + " and currEnd " + currEnd)
        else:
                out.write('no data' + '\n')
                        
    out.close()
    if b:
        b.close()
    if c:
        c.close()
    if r:
        r.close()
    if m:
        m.close()
    print("Finished formatting.")

def get_speech_style(rest):
    print("style is" + rest)
    if re.match(r'.*prg\d{3,4}sf', rest):
        return "Speaker Focus paragraph"
    elif re.match(r'.*prg\d{3,4}af1', rest):
        return "Designed Focus(1) paragraph"
    elif re.match(r'.*prg\d{3,4}af2', rest):
        return "Designed Focus(2) paragraph"
    elif re.match(r'.*prg\d{3,4}af3', rest):
        return "Designed Focus(3) paragraph"
    elif re.match(r'.*prg\d{3,4}_df', rest):
        return "Default focus paragraph"
    elif re.match(r'.*prg\d{3,4}', rest):
        return "Speech paragraph"
    elif re.match(r'.*sptn\d{3,4}_read', rest):
        return "Spontaneous vs. read speech"
    elif re.match(r'.*sptn\d{3,4}', rest):
        return "Spontaneous speech"
    elif re.match(r'.*phr\d{3,4}_d', rest):
        return "Declarative sentence"
    elif re.match(r'.*phr\d{3,4}_i', rest):
        return "Interrogative sentence"
    elif re.match(r'.*phr\d{3,4}_e', rest):
        return "Exclamatory sentence"
    elif re.match(r'.*phr\d{3,4}_c', rest):
        return "Carrier sentence"
    elif re.match(r'.*phr\d{3,4}_wd/np', rest):
        return "Word salad without punctuation"
    elif re.match(r'.*phr\d{3,4}_wd/p', rest):
        return "Word salad with punctuation"
    elif re.match(r'.*phr\d{3,4}_C', rest):
        return "Phrase China corpus"
    elif re.match(r'.*phr\d{3,4}_T', rest):
        return "Phrase Taiwan corpus"
    elif re.match(r'.*phr\d{3,4}', rest):
        return "Utterance or phrase"
    else:
        print("Couldn't match style!")
        return "Not found"

# there will always be 6 arguments because apply_task2_formatting.py is the pipeline
format_files(sys.argv[1], sys.argv[2], sys.argv[3], sys.argv[4], sys.argv[5], sys.argv[6])
