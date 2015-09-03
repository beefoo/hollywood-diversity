# -*- coding: utf-8 -*-

import csv
import json
import os

INPUT_FILE = '../data/people_box_office_top_50_movies_1995-2014.csv'
OUTPUT_DIR = '../data/'
WRITE_FILES = False

people_movie_roles = []
movies = []
people = []
roles = []

# Read data from csv
with open(INPUT_FILE, 'rb') as f:
    r = csv.reader(f, delimiter=',')
    next(r, None) # remove header
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

# Find unique movies
movies = [{'id': p['movie_id'], 'name': p['movie_name'], 'url': p['movie_url']} for p in people_movie_roles]
movies = {m['id']:m for m in movies}.values()
print('Found '+str(len(movies))+' movies.')

# Find unique people
people = [{'name': p['name'], 'url': p['url'], 'gender': p['gender'], 'race': p['race']} for p in people_movie_roles]
people = {p['name']:p for p in people}.values()
print('Found '+str(len(people))+' people.')
print('Found '+str(len([p for p in people if p['url']]))+' people with URLS.')

# Find roles in movies
for r in people_movie_roles:
    roles.append({
        'movie_name': r['movie_name'],
        'movie_url': r['movie_url'],
        'name': p['name'],
        'role': r['role']
    })
print('Found '+str(len(roles))+' roles.')

# Write JSON files

if WRITE_FILES:

    with open(OUTPUT_DIR + 'movies.json', 'w') as outfile:
        json.dump(movies, outfile)
        print('Successfully wrote movies to file: '+OUTPUT_DIR + 'movies.json')

    with open(OUTPUT_DIR + 'people.json', 'w') as outfile:
        json.dump(people, outfile)
        print('Successfully wrote people to file: '+OUTPUT_DIR + 'people.json')

    with open(OUTPUT_DIR + 'roles.json', 'w') as outfile:
        json.dump(roles, outfile)
        print('Successfully wrote roles to file: '+OUTPUT_DIR + 'roles.json')
