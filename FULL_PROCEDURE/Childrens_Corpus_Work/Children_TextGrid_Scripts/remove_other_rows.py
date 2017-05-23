#!/usr/bin/python

import sys

def label_txtgrid(f):
    # set initial progress values
    foundFourth = False
    foundItem = False

    # initialize new txtGrid file
    # remove creak_aligned extension
    fileTitle = f[:-9] + '-s.TextGrid'
    tg = open(fileTitle, 'w')

    # go through file
    with open(f) as file:
        for line in file:
            if not foundItem:
                if "size = " in line:
                    # change size to 1 instead of 4
                    tg.write("size = 1\n")
                elif "item []" in line:
                    foundItem = True
                    tg.write(line)
                else:
                    tg.write(line)
            # after the first few lines, skip until the fourht item is found
            elif not foundFourth:
                if "item [4]" in line:
                    tg.write("    item [1]:\n")
                    foundFourth = True
                else:
                    continue
            else:
                tg.write(line)


    tg.close()

label_txtgrid(sys.argv[1])