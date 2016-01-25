# -*- coding: utf-8 -*-

# Description:
#   Adds a column with a link to image search

# Example usage:
#   python add_image_link.py ../data/people_box_office_top_10_movies_2011-2015_imdb_subset.csv

import csv
import sys
import urllib

if len(sys.argv) < 1:
    print "Usage: %s <inputfile csv>" % sys.argv[0]
    sys.exit(1)

PEOPLE_FILE = sys.argv[1]

people = []
headers = []
col_name = 'image_search'

with open(PEOPLE_FILE, 'rb') as f:
    rows = csv.reader(f, delimiter=',')
    headers = next(rows, None) # remove header
    # init people list
    if col_name not in headers:
        headers.append(col_name)
    # populate people list
    for row in rows:
        person = {}
        for i, h in enumerate(headers):
            if (i >= len(row)): # doesn't exist, add as blank
                person[h] = ''
            else:
                person[h] = row[i]
        query = person['name'] + ' ' + person['movie_name']
        person[col_name] = 'https://www.google.com/search?newwindow=1&site=&tbm=isch&tbs=isz:l&sa=X&q=' + urllib.quote_plus(query)
        people.append(person)

# Write data back to file
with open(PEOPLE_FILE, 'wb') as f:
    w = csv.writer(f)
    w.writerow(headers)
    for p in people:
        row = []
        for h in headers:
            row.append(p[h])
        w.writerow(row)
    print('Successfully updated file: '+PEOPLE_FILE)
