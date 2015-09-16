# -*- coding: utf-8 -*-

# Example usage:
#   python rename_images.py ../data/people_box_office_top_50_movies_1995-2014_imdb_subset.csv http://s3.amazonaws.com/brianfoo_art/hollywood/

import csv
import sys

if len(sys.argv) < 2:
    print "Usage: %s <inputfile people csv> <url root dir>" % sys.argv[0]
    print "       people csv file must contain at least columns: imdb_id"
    sys.exit(1)

INPUT_FILE = sys.argv[1]
URL_ROOT_DIR = sys.argv[2]
overwrite_existing = False

people = []
filename_col = 'imdb_id'
required_cols = ['imdb_id', 'img']
headers = []

with open(INPUT_FILE, 'rb') as f:
    rows = csv.reader(f, delimiter=',')
    headers = next(rows, None) # remove header
    for col in required_cols:
        if col not in headers:
            print "People csv file must contain at least columns: imdb_id, img"
            sys.exit(1)
    # populate people list
    for row in rows:
        person = {}
        for i, h in enumerate(headers):
            person[h] = row[i]
        people.append(person)

for i, p in enumerate(people):
    if p['img'] and p['img'] != 'none':
        extension = p['img'].split('.')[-1]
        img = URL_ROOT_DIR + p[filename_col] + '.' + extension
        people[i]['img'] = img

with open(INPUT_FILE, 'wb') as f:
    w = csv.writer(f)
    w.writerow(headers)
    for p in people:
        row = []
        for h in headers:
            row.append(p[h])
        w.writerow(row)
    print('Successfully updated file: '+INPUT_FILE)
