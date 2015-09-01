# -*- coding: utf-8 -*-

# Data Sources:
#     First Names: http://www.ssa.gov/oact/babynames/limits.html
#     Surnames: http://www.census.gov/topics/population/genealogy/data/2000_surnames.html

import csv
import json
import os

INPUT_FILE = '../data/people_box_office_top_50_movies_1995-2014.csv'
NAMES_FILE = '../data/firstnames.csv'
SURNAMES_FILE = '../data/surnames.csv'
overwrite_existing = False

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
            'race': race,
            'fname': name.split(' ')[0].lower()
        })
fnames = set([p['fname'] for p in people_movie_roles])

# Read names from file
with open(NAMES_FILE) as data_file:
    names = json.load(data_file)

# Guess gender
g_match_count = 0
for fname in fnames:
    gender = 'u'
    matches = [n['g'] for n in names if n['n']==fname]
    if len(matches) > 0:
        g_match_count += 1
        for i, p in enumerate(people_movie_roles):
            if (overwrite_existing or not p['gender']) and p['fname']==fname:
                people_movie_roles[i]['gender'] = matches[0]

print('Found '+str(g_match_count)+' gender matches out of '+str(len(fnames))+' possible names.')

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
