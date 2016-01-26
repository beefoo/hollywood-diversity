# -*- coding: utf-8 -*-

# Description:
#   This file takes in a .csv file of movies and retrieves people involved in those movies from IMDB

# Example usage:
#   python imdb_get_people.py ../data/box_office_top_50_movies_1995-2014.csv ../data/people_box_office_top_50_movies_1995-2014_imdb.csv
#   python imdb_get_people.py ../data/box_office_top_10_movies_2006-2015.csv ../data/people_box_office_top_10_movies_2006-2015_imdb.csv

import csv
from imdb import IMDb
import os.path
import sys

MODE = 'append' # append, write

if len(sys.argv) < 2:
    print "Usage: %s <inputfile movies csv> <outputfile people csv>" % sys.argv[0]
    print "       movies csv file must contain at least columns: movie_id, name, imdb_id"
    sys.exit(1)

MOVIE_FILE = sys.argv[1]
PEOPLE_FILE = sys.argv[2]
roles = ['cast', 'producer', 'director', 'writer']

movies = []
movie_headers = []
people = []
people_headers = []
people_headers_to_add = ['movie_imdb_id', 'movie_name', 'role', 'order', 'name', 'imdb_id']

ia = IMDb()

# Read data from csv
with open(MOVIE_FILE, 'rb') as f:
    rows = csv.reader(f, delimiter=',')
    movie_headers = next(rows, None) # remove header
    if 'movie_id' not in movie_headers or 'name' not in movie_headers or 'imdb_id' not in movie_headers:
        print sys.argv[1] + " file must contain at least columns: movie_id, name, imdb_id"
        sys.exit(1)
    # populate movies list
    for row in rows:
        movie = {}
        for i, h in enumerate(movie_headers):
            movie[h] = row[i]
        movies.append(movie)

# Read people data from csv if exists
if os.path.isfile(PEOPLE_FILE):
    with open(PEOPLE_FILE, 'rb') as f:
        rows = csv.reader(f, delimiter=',')
        people_headers = next(rows, None) # remove header
        for h in people_headers_to_add:
            if h not in people_headers:
                people_headers.append(h)
        # populate people list
        for row in rows:
            person = {}
            for i, h in enumerate(people_headers):
                if (i >= len(row)): # doesn't exist, add as blank
                    person[h] = ''
                else:
                    person[h] = row[i]
            people.append(person)
if len(people_headers) <= 0:
    people_headers = people_headers_to_add

def imdb_key_exists(obj, key):
    try:
        test = obj[key]
        return True
    except KeyError:
        return False

def addRoleList(movie, role, role_list):
    global people
    global people_headers

    added_people = []
    for i, r in enumerate(role_list):
        person = {}
        for h in people_headers:
            person[h] = ''
        person['movie_imdb_id'] = movie['imdb_id']
        person['movie_name'] = movie['name']
        person['role'] = role
        person['order'] = i + 1
        person['name'] = r['name'].encode('utf-8')
        person['imdb_id'] = r.personID
        if len([p for p in added_people if p['imdb_id']==person['imdb_id']]) <= 0: # Ensure no duplicates
            people.append(person)
            added_people.append(person)

    return added_people

def addPeople(movie, imdb_movie):
    global roles

    added_people = []
    for role in roles:
        if imdb_key_exists(imdb_movie, role) and len(imdb_movie[role]) > 0:
            added_people.extend(addRoleList(movie, role, imdb_movie[role]))

    return added_people

def savePeople():
    global PEOPLE_FILE
    global people_headers
    global people

    with open(PEOPLE_FILE, 'wb') as f:
        w = csv.writer(f)
        w.writerow(people_headers)
        for p in people:
            row = []
            for h in people_headers:
                row.append(p[h])
            w.writerow(row)
        # print('Successfully wrote to file: '+PEOPLE_FILE)

def appendPeople(added_people):
    global PEOPLE_FILE
    global people_headers

    with open(PEOPLE_FILE, 'ab') as f:
        w = csv.writer(f)
        for p in added_people:
            row = []
            for h in people_headers:
                row.append(p[h])
            w.writerow(row)
        # print('Successfully updated file: '+PEOPLE_FILE)

for movie in movies:
    # Already processed this movie
    if len([p for p in people if p['movie_imdb_id']==movie['imdb_id']]) > 0:
        continue
    imdb_movie = ia.get_movie(movie['imdb_id'])
    if not imdb_movie:
        print('Could not find movie: '+movie['movie_id']+'. '+movie['name']+' ('+movie['imdb_id']+')')
    elif imdb_movie['kind'] != 'movie':
        print('This is not a movie: '+movie['movie_id']+'. '+movie['name']+' ('+movie['imdb_id']+')')
    else:
        print('Found movie: '+imdb_movie['long imdb canonical title'])
        added_people = addPeople(movie, imdb_movie)
        if MODE == 'write':
            savePeople()
        elif MODE == 'append':
            appendPeople(added_people)
