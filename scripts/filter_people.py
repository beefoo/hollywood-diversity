# -*- coding: utf-8 -*-

# Example usage:
#   python filter_people.py ../data/people_box_office_top_50_movies_1995-2014_imdb.csv ../data/people_box_office_top_50_movies_1995-2014_imdb_subset.csv

import csv
import sys

if len(sys.argv) < 2:
    print "Usage: %s <inputfile people csv> <outputfile people csv>" % sys.argv[0]
    print "       movies csv file must contain at least columns: movie_id, name, imdb_id"
    sys.exit(1)

INPUT_FILE = sys.argv[1]
OUTPUT_FILE = sys.argv[2]
filters = [
    {'column': 'role', 'value': 'cast', 'limit': 6},
    {'column': 'role', 'value': 'producer', 'limit': 6},
    {'column': 'role', 'value': 'writer', 'limit': 6}
]

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
        is_valid = True
        for f in filters:
            if person[f['column']] == f['value'] and int(person['order']) > f['limit']:
                is_valid = False
                break
        if is_valid:
            people.append(person)

with open(OUTPUT_FILE, 'wb') as f:
    w = csv.writer(f)
    w.writerow(headers)
    for p in people:
        row = []
        for h in headers:
            row.append(p[h])
        w.writerow(row)
    print('Successfully wrote to file: '+OUTPUT_FILE)
