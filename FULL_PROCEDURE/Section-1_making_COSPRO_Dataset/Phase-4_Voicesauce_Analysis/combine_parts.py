import re
import sys
from os import listdir


def combine_parts(partLength, directory, outPath):

    # check that partLength is an integer
    try:
        partLength = int(partLength)
        print("Part length is " + str(partLength))
    except:
        raise ValueError("Inputted partLength is not an integer.")

    currName = ''
    out = ''
    addedTime = 0
    filesList = listdir(directory)
    for f in filesList:
        if "DS_Store" in f or "combined" in f:
            continue
        print("Working file " + f)

        # get part and new name
        extension = re.sub(r'.*part\d+(\..*)', r'\1', f)
        partNo = int(re.sub(r'.*part(\d+)\..*', r'\1', f))
        newName = re.sub(r'(.*)part.*', r'\1', f)

        # if it's part 0, make a new out file with the new name
        if partNo == 0:
            if newName == currName:
                # this should never be the case
                raise ValueError("File is part 0 but has the same name as previous file.")
            else:
                if out:
                    out.close()
                outName = outPath + newName + extension
                out = open(outName, 'w')

        # get part addedTime
        addedTime = partNo * partLength
        print("added time is " + str(addedTime))

        with open(f, 'r') as curr:
            first = True
            for line in curr:
                # this is for creak files only

                if first:
                    # skip the first line of each file
                    first = False
                    continue
                else:
                    try:
                        [timeStamp, val] = line.split(',')
                    except ValueError:
                        raise ValueError("Line is not formatted like a creak file.")
                    timeStamp = str(float(timeStamp) + float(addedTime))
                    out.write(timeStamp + ',' + val)

    out.close()

combine_parts(sys.argv[1], sys.argv[2], sys.argv[3])