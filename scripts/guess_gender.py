#!/usr/bin/env python

import csv
import os

INPUT_FILE = '../data/people_box_office_top_50_movies_1995-2014.csv'

people_movie_roles = []
names = []
headers = []

# Read data from csv
with open(INPUT_FILE, 'rb') as f:
    r = csv.reader(f, delimiter=',')
    headers = next(r, None) # remove header
    for movie_id, movie_name, movie_url, role, name, url, gender, race in r:
        people_movie_roles.append({
            'movie_id': int(movie_id),
            'movie_name': movie_name,
            'movie_url': movie_url,
            'role': role,
            'name': name,
            'url': url,
            'gender': gender,
            'race': race
        })
names = set([p['name'] for p in people_movie_roles])

# Guess gender
for name in names:
    gender = 'u'

# Write data back to file
with open(INPUT_FILE, 'wb') as f:
    w = csv.writer(f)
    w.writerow(headers)
    for p in people_movie_roles:
        row = []
        for h in headers:
            row.append(p[h])
        w.writerow(row)
    print('Successfully updated file: '+INPUT_FILE)
