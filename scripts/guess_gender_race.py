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
overwrite_existing = True

people_movie_roles = []
names = []
surnames = []
headers = []

def is_number(s):
    try:
        float(s)
        return True
    except ValueError:
        return False

def parse_float(s):
    if is_number(s):
        return float(s)
    else:
        return 0.0

# Read data from csv
with open(INPUT_FILE, 'rb') as f:
    r = csv.reader(f, delimiter=',')
    headers = next(r, None) # remove header
    for movie_id, movie_name, movie_url, role, name, url, gender, race in r:
        name_parts = name.lower().split(' ')
        people_movie_roles.append({
            'movie_id': int(movie_id),
            'movie_name': movie_name,
            'movie_url': movie_url,
            'role': role,
            'name': name,
            'url': url,
            'gender': gender,
            'race': race,
            'fname': name_parts[0],
            'lnames': name_parts[1:][::-1]
        })
fnames = set([p['fname'] for p in people_movie_roles])

# Read names from file
with open(NAMES_FILE, 'rb') as f:
    r = csv.reader(f, delimiter=',')
    for name, gender in r:
        names.append({
            'name': name,
            'gender': gender
        })

# Read surnames from file
race_percent_threshold = 25;
with open(SURNAMES_FILE, 'rb') as f:
    r = csv.reader(f, delimiter=',')
    next(r, None) # remove header
    for name,rank,count,prop100k,cum_prop100k,pctwhite,pctblack,pctapi,pctaian,pct2prace,pcthispanic in r:
        races = [
            {'key': 'w', 'pct': parse_float(pctwhite)}, # white
            {'key': 'b', 'pct': parse_float(pctblack)}, # black
            {'key': 'a', 'pct': parse_float(pctapi)}, # asian, pacific islander
            {'key': 'h', 'pct': parse_float(pcthispanic)}, # hispanic, non-white
            {'key': 'o', 'pct': parse_float(pctaian)}, # native american/alaskan
            {'key': 'o', 'pct': parse_float(pct2prace)} # 2 or more races
        ]
        races = sorted(races, key=lambda k: k['pct'], reverse=True)
        race = ''
        if races[0]['pct'] > race_percent_threshold:
            race = races[0]['key']
        surnames.append({
            'name': name.lower(),
            'race': race
        })

# Guess gender
g_match_count = 0
for fname in fnames:
    gender = 'u'
    matches = [n['gender'] for n in names if n['name']==fname]
    if len(matches) > 0:
        g_match_count += 1
        for i, p in enumerate(people_movie_roles):
            if (overwrite_existing or not p['gender']) and p['fname']==fname:
                people_movie_roles[i]['gender'] = matches[0]

print('Found '+str(g_match_count)+' gender matches out of '+str(len(fnames))+' possible names.')

# Guess race
r_match_count = 0
for i, p in enumerate(people_movie_roles):
    for ln in p['lnames']:
        matches = [n['race'] for n in surnames if n['name']==ln]
        if len(matches) > 0 and matches[0]:
            r_match_count += 1
            if (overwrite_existing or not p['race']):
                people_movie_roles[i]['race'] = matches[0]
            break

print('Found '+str(r_match_count)+' race matches out of '+str(len(people_movie_roles))+' possible names.')

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
