# -*- coding: utf-8 -*-

# Example usage:
#   python generate_json.py ../data/box_office_top_50_movies_1995-2014.csv ../data/people_box_office_top_50_movies_1995-2014_imdb_subset.csv

import csv
import json
import sys

if len(sys.argv) < 2:
    print "Usage: %s <inputfile movie csv> <inputfile people-roles csv>" % sys.argv[0]
    sys.exit(1)

MOVIE_FILE = sys.argv[1]
PEOPLE_FILE = sys.argv[2]
OUTPUT_DIR = '../data/'
WRITE_FILES = True

movie_required_headers = ['movie_id', 'wiki_name', 'imdb_id']
people_required_headers = ['name', 'imdb_id', 'gender', 'race']
roles_required_headers = ['movie_id', 'movie_name', 'role', 'imdb_id']

movies = []
people = []
roles = []

# Read movies from csv
with open(MOVIE_FILE, 'rb') as f:
    rows = csv.reader(f, delimiter=',')
    headers = next(rows, None) # remove header
    # add new headers if not exist
    for h in movie_required_headers:
        if h not in headers:
            print "The following movie fields are required: " + movie_required_headers.join(", ")
            sys.exit(1)
    # populate movies list
    for row in rows:
        movie = {}
        for h in movie_required_headers:
            i = headers.index(h)
            movie[h] = row[i]
        movies.append(movie)

# Read movies from csv
with open(PEOPLE_FILE, 'rb') as f:
    rows = csv.reader(f, delimiter=',')
    headers = next(rows, None) # remove header
    # add new headers if not exist
    required_headers = people_required_headers + roles_required_headers
    for h in required_headers:
        if h not in headers:
            print "The following role/people fields are required: " + ", ".join(required_headers)
            sys.exit(1)
    # populate people/roles lists
    for row in rows:
        # add person
        person = {}
        for h in people_required_headers:
            i = headers.index(h)
            person[h] = row[i]
        people.append(person)
        # add role
        role = {}
        for h in roles_required_headers:
            i = headers.index(h)
            role[h] = row[i]
        roles.append(role)

# Find unique people
people = {p['imdb_id']:p for p in people}.values()

# Report counts
print('Found '+str(len(movies))+' movies.')
print('Found '+str(len(people))+' people.')
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
