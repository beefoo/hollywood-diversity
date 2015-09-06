# -*- coding: utf-8 -*-

# Example usage:
#   python remove_duplicates.py ../data/people_box_office_top_50_movies_1995-2014_imdb.csv
import csv
import sys

if len(sys.argv) < 1:
    print "Usage: %s <inputfile people csv>" % sys.argv[0]
    print "       movies csv file must contain at least columns: movie_id, name, imdb_id"
    sys.exit(1)

INPUT_FILE = sys.argv[1]

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
        # check if person/role already exists
        if len([p for p in people if person['movie_id']==p['movie_id'] and person['role']==p['role'] and person['imdb_id']==p['imdb_id']]) <= 0:
            people.append(person)

with open(INPUT_FILE, 'wb') as f:
    w = csv.writer(f)
    w.writerow(headers)
    for p in people:
        row = []
        for h in headers:
            row.append(p[h])
        w.writerow(row)
    print('Successfully updated file: '+INPUT_FILE)
