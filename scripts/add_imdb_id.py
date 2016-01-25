# -*- coding: utf-8 -*-

# Example usage:
#   python add_imdb_id.py ../data/box_office_top_10_movies_2011-2015.csv ../data/people_box_office_top_10_movies_2011-2015_imdb_subset.csv

import csv
import sys

if len(sys.argv) < 2:
    print "Usage: %s <inputfile movie csv> <inputfile people csv>" % sys.argv[0]
    sys.exit(1)

MOVIE_FILE = sys.argv[1]
PEOPLE_FILE = sys.argv[2]
overwrite_existing = False

movies = []
people = []
people_headers = []

with open(MOVIE_FILE, 'rb') as f:
    rows = csv.reader(f, delimiter=',')
    headers = next(rows, None) # remove header
    # populate movie list
    for row in rows:
        movie = {}
        for i, h in enumerate(headers):
            movie[h] = row[i]
        movies.append(movie)

with open(PEOPLE_FILE, 'rb') as f:
    rows = csv.reader(f, delimiter=',')
    people_headers = next(rows, None) # remove header
    # populate people list
    for row in rows:
        person = {}
        for i, h in enumerate(people_headers):
            person[h] = row[i]
        person['movie_imdb_id'] = next(iter([m['imdb_id'] for m in movies if m['movie_id']==person['movie_id']]), False)
        people.append(person)

with open(PEOPLE_FILE, 'wb') as f:
    w = csv.writer(f)
    w.writerow(people_headers)
    for p in people:
        row = []
        for h in people_headers:
            row.append(p[h])
        w.writerow(row)

print "Updated %s people in file %s" % (len(people), PEOPLE_FILE)
