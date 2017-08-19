#!/usr/bin/python

# paste spreadsheet files

import sys
import re
from os import listdir, getcwd, chdir
from os.path import isfile, relpath, dirname, abspath
from itertools import cycle


def paste_files(directory, out_name, log_name):

    refdirectory = dirname('/Users/John/Documents/Phonetics_Lab_Summer_2017')
    if isfile(log_name):
        log = open(log_name, 'a')
    else:
        log = open(log_name, 'w')

    # otherwise, it should be a directory of .creak files
    if not isfile(directory): 
        print("directory")
            
        # Get all files in directory
        files = listdir(directory)
        # print(files)

        # check that correct type of files are in directory
        if ".t2.txt" in files[3]:
            
            chdir(directory)

            # create outFile
            out = open(out_name, 'w')

            first = True
            # go through files
            for f in files:
                if "DS" in f:
                    continue
                if not files:
                    continue
                sys.stdout.write('\r')
                sys.stdout.write("Adding " + f)
                # f = abspath(f)
                # print "abspath " + f
                with open(f, 'r') as curr:
                    first_line = True
                    for line in curr:
                        # print "line is " + line
                        # print headlines if first iteration
                        if first_line:
                            first_line = False
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

paste_files(sys.argv[1], sys.argv[2], sys.argv[3])