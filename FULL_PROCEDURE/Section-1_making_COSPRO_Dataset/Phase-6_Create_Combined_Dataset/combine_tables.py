 #!/usr/bin/python

# paste spreadsheet files

import sys
import re
from os import listdir, getcwd, chdir
from os.path import isfile, relpath, dirname, abspath
from itertools import cycle

def paste_files(directory, outName):

    refdirectory = dirname('/Users/John/Desktop/COSPRO_DATA_BIN/Task2_Formatting')
        
    # otherwise, it should be a directory of .creak files
    if not isfile(directory): 
        print("directory")
            
        # Get all files in directory
        files = listdir(directory)
        print(files)


        # check that correct type of files are in directory
        if ".t2.txt" in files[1]:
            
            chdir(directory)

            # create outFile
            out = open(outName, 'w')

            first = True
            # go through files
            for f in files:
                if "DS" in f:
                    continue
                print("adding " + f)
                # f = abspath(f)
                # print "abspath " + f
                with open(f, 'r') as curr:
                    firstLine = True
                    for line in curr:
                        # print "line is " + line
                        # print headlines if first iteration
                        if firstLine:
                            firstLine = False
                            if first:
                                first = False
                                # clean up line
                                line = line.rstrip()
                                if line:
                                    out.write(line + '\n')
                            else:
                                continue

                        else:
                            # clean up line
                            line = line.rstrip()
                            if line:
                                out.write(line + '\n')
            out.close()

paste_files(sys.argv[1], sys.argv[2])