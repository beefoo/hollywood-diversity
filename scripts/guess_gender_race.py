# -*- coding: utf-8 -*-

# Description:
#   Attempts to populate columns "gender" and "race" based on "name" in csv

# Example usage:
#   python guess_gender_race.py ../data/people_box_office_top_50_movies_1995-2014_imdb_subset.csv
#       .csv file must have at least column "name"

# Data Sources:
#     First Names: http://www.ssa.gov/oact/babynames/limits.html
#     Surnames: http://www.census.gov/topics/population/genealogy/data/2000_surnames.html

import csv
import sys

if len(sys.argv) < 1:
    print "Usage: %s <inputfile csv>" % sys.argv[0]
    sys.exit(1)

PEOPLE_FILE = sys.argv[1]
NAMES_FILE = '../data/firstnames.csv'
SURNAMES_FILE = '../data/surnames.csv'
overwrite_existing = True

people = []
headers = []
headers_to_add = ['gender', 'race']

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

with open(PEOPLE_FILE, 'rb') as f:
    rows = csv.reader(f, delimiter=',')
    headers = next(rows, None) # remove header
    if 'name' not in headers:
        print PEOPLE_FILE + " must have column <name>"
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
        # determine first and last names
        name_parts = person['name'].lower().split(' ')
        person['fname'] = name_parts[0]
        person['lnames'] = name_parts[1:][::-1]
        people.append(person)

fnames = set([p['fname'] for p in people])
names = []
surnames = []

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
    matches = [n['gender'] for n in names if n['name']==fname]
    if len(matches) > 0:
        g_match_count += 1
        for i, p in enumerate(people):
            if (overwrite_existing or not p['gender']) and p['fname']==fname:
                people[i]['gender'] = matches[0]

print('Found '+str(g_match_count)+' gender matches out of '+str(len(fnames))+' possible names.')

# Guess race
r_match_count = 0
for i, p in enumerate(people):
    for ln in p['lnames']:
        matches = [n['race'] for n in surnames if n['name']==ln]
        if len(matches) > 0 and matches[0]:
            r_match_count += 1
            if (overwrite_existing or not p['race']):
                people[i]['race'] = matches[0]
            break

print('Found '+str(r_match_count)+' race matches out of '+str(len(people))+' possible names.')

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
