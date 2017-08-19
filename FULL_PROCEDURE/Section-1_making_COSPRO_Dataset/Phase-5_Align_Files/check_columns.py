#!/usr/bin/python
import re
import sys


def check_columns(file, log_name):
    print("Starting")
    bad = False
    with open(file, 'r') as f:
        log = open(log_name, 'w')
        columns = 0
        line_num = 0
        file_line = 0
        filename = ''
        for line in f:
            line_num += 1
            file_line += 1
            # log.write("Line number " + str(line_num) + '\n')
            parts = re.split('\t', line)
            if filename != parts[0]:
                filename = parts[0]
                file_line = 2
            if columns == 0:
                columns = len(parts)
                print("There are " + str(columns) + " columns in the first row")

            sys.stdout.write("\rLine number " + str(line_num))
            if len(parts) != columns:
                bad = True
                log.write(str(line_num) + '\n')
                log.write("Line does not have same number of columns as previous line!\n")
                log.write("Previous line (" + str(file_line-1) + ") had " + str(columns) + '\n')
                log.write("Current line (" + str(file_line) + ") has " + str(len(parts)) + '\n')
                log.write(parts[0] + ', ' + parts[1] + ', ' + parts[2] + '\n')
                log.write("------------------------------\n")
                columns = len(parts)
            # if line_num == 50:
            #     break
        if not bad:
            sys.stdout.write("\nAll columns are the same length (" + str(columns) + ")")
            log.write("All columns are the same length (" + str(columns) + ")")
    sys.stdout.write('\n')
    log.close()

check_columns(sys.argv[1], sys.argv[2])
