#!/usr/bin/env python

import csv
import sys


for line in csv.reader(sys.stdin):

    fields = [word.replace('"', '') for word in line]
    mfg = fields[3]
    amt_usd_enc = fields[48]
    try:
        if mfg and amt_usd_enc:
            amt_usd = float(amt_usd_enc)
            print '{mfg}\t{amt}'.format(mfg=mfg, amt=amt_usd)
    except:
        # just skip this line
        pass
