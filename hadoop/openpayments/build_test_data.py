#!/usr/bin/env python
#
# A simple script to save NUM lines from the huge dataset into a smaller file for simple tests
#
# Usage: build_test_data.py [outfile]

from __future__ import print_function
import random
import sys

__author__ = 'marco'


FILE_NAME = 'data/OPPR_ALL_DTL_GNRL_12192014.csv'
NUM = 100
SKIP = 50000

outfile = 'data/test.csv'
if len(sys.argv) > 1:
    outfile = sys.argv[1]

print("Extracting {num} records from {src} to {dest}".format(num=NUM, src=FILE_NAME, dest=outfile))
with open(FILE_NAME, 'r') as src:
    with open(outfile, 'w') as dest:
        for _ in xrange(NUM):
            line = src.readline()
            dest.writelines(line)
            print('.', end="")
            for _ in xrange(random.randint(100, SKIP)):
                src.readline()
print("Finished")
