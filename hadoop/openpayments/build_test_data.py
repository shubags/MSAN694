#!/usr/bin/env python
#
# A simple script to save NUM lines from the huge dataset into a smaller file for simple tests
#
# Usage: build_test_data.py [outfile]

from __future__ import print_function
import argparse
import random
import sys

__author__ = 'marco'

FILE_NAME = 'data/OPPR_ALL_DTL_GNRL_12192014.csv'
NUM = 100
SKIP = 50000


def parse_args():
    parser = argparse.ArgumentParser()
    parser.add_argument("--out", required=True, help="Output file")
    parser.add_argument("--lines", default=NUM, type=int, help="Number of lines to extract, "
                                                               "optional")
    parser.add_argument("--skip", default=SKIP, type=int,
                        help="Number of lines to skip, between extracted lines; this "
                             "varies randomly, between 100 and the skip value given here")
    return parser.parse_args()


def progress_pct(count, tot):
    return 100.0 * float(count) / float(tot)


def main(config):
    num = config.lines
    outfile = config.out
    max_skip = config.skip
    print("Extracting {num} records from {src} to {dest}".format(num=num, src=FILE_NAME,
                                                                 dest=outfile))
    last_progress = 0
    with open(FILE_NAME, 'r') as src:
        with open(outfile, 'w') as dest:
            # Skip the first line with the field names
            src.readline()
            for lineno in xrange(num):
                line = src.readline()
                dest.writelines(line)
                progress = progress_pct(lineno, num)
                if progress - last_progress > 5:
                    print('%.2f%%' % (progress,))
                    sys.stdout.flush()
                    last_progress = progress
                for _ in xrange(random.randint(100, max_skip)):
                    src.readline()
    print("Finished")


if __name__ == "__main__":
    main(parse_args())
