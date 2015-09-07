# -*- coding: utf-8 -*-

# Description:
#   This file takes in a .csv file of movies and retrieves genres of those movies from IMDB

# Example usage:
#   python imdb_get_genres.py ../data/box_office_top_50_movies_1995-2014.csv ../data/genres_box_office_top_50_movies_1995-2014.csv

import csv
from imdb import IMDb
import os.path
import sys

MODE = 'append' # append, write

if len(sys.argv) < 2:
    print "Usage: %s <inputfile movies csv> <outputfile genre csv>" % sys.argv[0]
    print "       movies csv file must contain at least columns: movie_id, name, imdb_id"
    sys.exit(1)

MOVIE_FILE = sys.argv[1]
GENRE_FILE = sys.argv[2]

movies = []
movie_headers = []
genres = []
genre_headers = []
genre_headers_to_add = ['movie_id', 'movie_name', 'genre']

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

# Read genre data from csv if exists
if os.path.isfile(GENRE_FILE):
    with open(GENRE_FILE, 'rb') as f:
        rows = csv.reader(f, delimiter=',')
        genre_headers = next(rows, None) # remove header
        for h in genre_headers_to_add:
            if h not in genre_headers:
                genre_headers.append(h)
        # populate genre list
        for row in rows:
            genre = {}
            for i, h in enumerate(genre_headers):
                if (i >= len(row)): # doesn't exist, add as blank
                    genre[h] = ''
                else:
                    genre[h] = row[i]
            genres.append(genre)
if len(genre_headers) <= 0:
    genre_headers = genre_headers_to_add

def imdb_key_exists(obj, key):
    try:
        test = obj[key]
        return True
    except KeyError:
        return False

def addGenres(movie, imdb_movie):
    global genres
    global genre_headers

    added_genres = []
    if imdb_key_exists(imdb_movie, 'genres') and len(imdb_movie['genres']) > 0:
        for g in imdb_movie['genres']:
            genre = {}
            for h in genre_headers:
                genre[h] = ''
            genre['movie_id'] = movie['movie_id']
            genre['movie_name'] = movie['name']
            genre['genre'] = g
            added_genres.append(genre)
            genres.append(genre)

    return added_genres

def saveGenres():
    global GENRE_FILE
    global genre_headers
    global genres

    with open(GENRE_FILE, 'wb') as f:
        w = csv.writer(f)
        w.writerow(genre_headers)
        for g in genres:
            row = []
            for h in genre_headers:
                row.append(g[h])
            w.writerow(row)
        # print('Successfully wrote to file: '+GENRE_FILE)

def appendGenres(added_genres):
    global GENRE_FILE
    global genre_headers

    with open(GENRE_FILE, 'ab') as f:
        w = csv.writer(f)
        for g in added_genres:
            row = []
            for h in genre_headers:
                row.append(g[h])
            w.writerow(row)
        # print('Successfully updated file: '+GENRE_FILE)

for movie in movies:
    # Already processed this movie
    if len([g for g in genres if g['movie_id']==movie['movie_id']]) > 0:
        continue
    imdb_movie = ia.get_movie(movie['imdb_id'])
    if not imdb_movie:
        print('Could not find movie: '+movie['movie_id']+'. '+movie['name']+' ('+movie['imdb_id']+')')
    elif imdb_movie['kind'] != 'movie':
        print('This is not a movie: '+movie['movie_id']+'. '+movie['name']+' ('+movie['imdb_id']+')')
    else:
        print('Found movie: '+imdb_movie['long imdb canonical title'])
        added_genres = addGenres(movie, imdb_movie)
        if MODE == 'write':
            saveGenres()
        elif MODE == 'append':
            appendGenres(added_genres)
