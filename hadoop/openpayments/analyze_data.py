#!/usr/bin/env python

from __future__ import print_function
import json
import sys

__author__ = 'marco'


FILE_NAME = 'data/OPPR_ALL_DTL_GNRL_12192014.csv'

outfile = 'data/structure.txt'
if len(sys.argv) > 1:
    outfile = sys.argv[1]

print("Extracting records structure in {src} to {dest}".format(src=FILE_NAME, dest=outfile))
with open(FILE_NAME, 'r') as src:
    with open(outfile, 'w') as dest:
        line = src.readline()
        fields = line.split(',')
        structure = {}
        for i, field in enumerate(fields):
            structure[i] = field.replace('"', '')
        st = json.dumps(structure, indent=4)
        print(st)
        dest.write(st)
