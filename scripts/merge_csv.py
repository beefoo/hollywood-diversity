# -*- coding: utf-8 -*-

# Description:
#   Merge one csv file into another

# Example usage:
#   python merge_csv.py ../data/people_box_office_top_10_movies_2011-2015_imdb_subset.csv ../data/people_box_office_top_10_movies_2011-2015_imdb_subset_classifications.csv gender,races,note,reference_url imdb_id

import csv
import sys

if len(sys.argv) < 4:
    print "Usage: %s <primary csv> <secondary csv> <fields to merge> <merge id>" % sys.argv[0]
    sys.exit(1)

PRIMARY_FILE = sys.argv[1]
SECONDARY_FILE = sys.argv[2]
FIELDS_TO_MERGE = sys.argv[3]
MERGE_ID = sys.argv[4]

people = []
headers = []
headers_to_add = FIELDS_TO_MERGE.split(',')
data_to_merge = []

with open(PRIMARY_FILE, 'rb') as f:
    rows = csv.reader(f, delimiter=',')
    headers = next(rows, None) # remove header

    if MERGE_ID not in headers:
        print PRIMARY_FILE + " must have column <" + MERGE_ID + ">"
        sys.exit(1)
    # init people list
    for h in headers_to_add:
        if h not in headers:
            headers.append(h)
    # populate people list
    for row in rows:
        person = {}
        for i, h in enumerate(headers):
            if (i >= len(row)): # doesn't exist, add as blank
                person[h] = ''
            else:
                person[h] = row[i]
        people.append(person)

with open(SECONDARY_FILE, 'rb') as f:
    rows = csv.reader(f, delimiter=',')
    _headers = next(rows, None) # remove header

    if MERGE_ID not in _headers:
        print SECONDARY_FILE + " must have column <" + MERGE_ID + ">"
        sys.exit(1)

    # populate people list
    for row in rows:
        data = {}
        for i, h in enumerate(_headers):
            if h in headers_to_add or h==MERGE_ID:
                data[h] = row[i]
        for i, p in enumerate(people):
            if p[MERGE_ID] == data[MERGE_ID]:
                people[i].update(data)

# Write data back to file
with open(PRIMARY_FILE, 'wb') as f:
    w = csv.writer(f)
    w.writerow(headers)
    for p in people:
        row = []
        for h in headers:
            row.append(p[h])
        w.writerow(row)
    print('Successfully updated file: '+PRIMARY_FILE)
