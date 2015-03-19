#!/usr/bin/env python

import sys


for line in sys.stdin:
    # skip header line
    if line.startswith('#'):
        continue
    fields = [word.replace('"', '') for word in line.strip().split(',')]
    mfg = fields[3]
    amt_usd_enc = fields[48]
    try:
        if mfg and amt_usd_enc:
            amt_usd = float(amt_usd_enc)
            print '{mfg}\t{amt}'.format(mfg=mfg, amt=amt_usd)
    except:
        # just skip this line
        pass
