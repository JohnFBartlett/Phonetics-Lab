#!/usr/bin/python

import sys, re
from os import listdir
from os.path import isfile, relpath, dirname
from itertools import cycle

def split_measures(packedFile, outpath):

    if isfile(packedFile):
        if ".txt" in packedFile:
            name = ''
            with open(packedFile, 'r') as m:
                # get header line
                header = next(m)
                for line in m:
                    parts = line.split('\t')
                    newName = parts[0]
                    # cut off mat extension
                    newName = newName[:-3] + 'measures_aligned'
                    if newName != name:
                        out = open(outpath + newName, 'w')
                        out.write(header)
                        name = newName
                        print "Splitting file " + name
                    # write line
                    out.write(line)
            out.close()

        else:
            raise ValueError("Wrong file type: need .txt")

split_measures(sys.argv[1], sys.argv[2])