#!/usr/bin/python

import sys
import re

front = re.sub(r'(.*part)\d{1}.mat', r'\1', sys.argv[1]) 
# if it doesn't get a substring, just return th initial argument
if front == sys.argv[1]:
    print front
else:
    back = re.sub(r'.*part(\d{1}.mat)', r'\1', sys.argv[1]) 
    print front + '0' + back
