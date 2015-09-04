# -*- coding: utf-8 -*-

import csv
import os
import sys
import wikipedia

INPUT_FILE = '../data/people_box_office_top_50_movies_1995-2014.csv'
UPDATE_FILE = True

def is_int(s):
    try:
        int(s)
        return True
    except ValueError:
        return False

people_movie_roles = []
headers = []
people = []

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

# Find unique people
people_names = set([p['name'] for p in people_movie_roles if not p['url']])
print('Found '+str(len(people_names))+' people without URLs.')

# Add URLs if found
matches = 0
for n in people_names:
    page = False
    try:
        page = wikipedia.page(n)
    # except wikipedia.exceptions.DisambiguationError as e:
    #     for i, o in enumerate(e.options):
    #         print(str(i)+'. '+o)
    #     selection = raw_input('Your selection for '+n+': ')
    #     if is_int(selection):
    #         page = wikipedia.page(e.options[selection])
    except:
        page = False

    if page and page.title.split(' ')[0] == n.split(' ')[0]:
        print('Found match: '+n.decode('utf-8')+' -> '+page.url.decode('utf-8'))
        matches += 1
        for i, p in enumerate(people_movie_roles):
            if p['name']==n:
                people_movie_roles[i]['url'] = page.url
    else:
        print('No match for '+n.decode('utf-8'))
print('Found '+str(matches)+' matches.')

# Write data back to file
if UPDATE_FILE:
    with open(INPUT_FILE, 'wb') as f:
        w = csv.writer(f)
        w.writerow(headers)
        for p in people_movie_roles:
            row = []
            for h in headers:
                row.append(p[h])
            w.writerow(row)
        print('Successfully updated file: '+INPUT_FILE)
