# -*- coding: utf-8 -*-

# Example usage:
#   python remove_roles.py ../data/people_box_office_top_10_movies_2011-2015_imdb_subset.csv producer

import csv
import sys

if len(sys.argv) < 2:
    print "Usage: %s <inputfile people csv> <role name>" % sys.argv[0]
    print "       movies csv file must contain at least columns: role"
    sys.exit(1)

INPUT_FILE = sys.argv[1]
ROLE = sys.argv[2]

people = []
headers = []

with open(INPUT_FILE, 'rb') as f:
    rows = csv.reader(f, delimiter=',')
    headers = next(rows, None) # remove header
    # populate people list
    for row in rows:
        person = {}
        for i, h in enumerate(headers):
            person[h] = row[i]
        # check if person is filtered out
        if person['role'] != ROLE:
            people.append(person)

with open(INPUT_FILE, 'wb') as f:
    w = csv.writer(f)
    w.writerow(headers)
    for p in people:
        row = []
        for h in headers:
            row.append(p[h])
        w.writerow(row)
    print('Successfully wrote to file: '+INPUT_FILE)
