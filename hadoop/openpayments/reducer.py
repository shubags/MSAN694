#!/usr/bin/env python

import sys


key = None
sum = 0.0
for line in sys.stdin:
    mfg, value = line.strip().split('\t')
    if key is None:
        key = mfg
    if mfg and mfg != key:
        # We are on the first record for a new key, print and reset the sum
        print("{}\t{}".format(key, sum))
        sum = 0.0
        key = mfg
    try:
        sum += float(value)
    except ValueError:
        # Just ignore malformed records
        continue

# don't forget the last record!
if key:
    print "{}\t{}".format(key, sum)
