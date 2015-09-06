# -*- coding: utf-8 -*-

# Usage:
#   python sort_csv.py ../data/people_box_office_top_50_movies_1995-2014_imdb.csv movie_id

import csv
import sys

if len(sys.argv) < 2:
    print "Usage: %s <input file> <sort by>" % sys.argv[0]
    sys.exit(1)

INPUT_FILE = sys.argv[1]
SORT_BY = sys.argv[2]

items = []
headers = []

# Read data from csv
with open(INPUT_FILE, 'rb') as f:
    rows = csv.reader(f, delimiter=',')
    headers = next(rows, None) # remove header
    if SORT_BY not in headers:
        print SORT_BY + " does not exist in csv header"
        sys.exit(1)
    # populate data
    for row in rows:
        item = {}
        for i, h in enumerate(headers):
            if h==SORT_BY and row[i].isdigit():
                item[h] = int(row[i])
            else:
                item[h] = row[i]
        items.append(item)

items = sorted(items, key=lambda k: k[SORT_BY])

with open(INPUT_FILE, 'wb') as f:
    w = csv.writer(f)
    w.writerow(headers)
    for i in items:
        row = []
        for h in headers:
            row.append(i[h])
        w.writerow(row)
    print ('Successfully sorted file: '+INPUT_FILE)
