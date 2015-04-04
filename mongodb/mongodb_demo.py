# MongoDb demo script - there is a lot more to connecting to a Distributed DB
#
# See the code in my Sentinel project (http://github.com/massenz/sentinel) for an
# example of how it should be done
#
# DON'T DO THIS IN REAL PRODUCTION CODE

from __future__ import print_function
import argparse
import csv
from pymongo import MongoClient

__author__ = 'marco'


def to_dict(record):
    record = [field.replace('"', '') for field in record]
    return {
        'first_name': record[8],
        'last_name': record[10],
        'teaching_hospital': record[6]
    }


def parse_args():
    parser = argparse.ArgumentParser()
    parser.add_argument('--dburi', default='mongodb://localhost/test')
    parser.add_argument('--file', required=True)
    parser.add_argument('--db', default='openpayments')
    return parser.parse_args()


def find_id(coll, record):
    result = coll.find_one(record)
    if result:
        return result.get('_id')
    return None


def parse_file(filename):
    with open(filename, 'r') as datafile:
        for line in csv.reader(datafile):
            yield line


def main():
    config = parse_args()
    # Open a connection to the DB Server
    c = MongoClient(config.dburi)
    # The actual db name can be accessed via both dot-notation (c.db) or []
    db = c[config.db]
    # Within the db namespace, the collection is equally accessible via dotted notation or by name
    coll = db.data
    count = 0
    for record in parse_file(config.file):
        doc = to_dict(record)
        if find_id(coll, doc) is None:
            coll.insert(doc)
            count += 1
    print("Inserted {} records in {}".format(count, coll))

if __name__ == '__main__':
    main()
