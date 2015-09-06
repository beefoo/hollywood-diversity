# -*- coding: utf-8 -*-

# Description:
#   This file takes in a .csv file of movies and adds IMDB information to it.
#   The script prompts user for input if there are ambiguities for a title.
#
# Example usage:
#   python imdb_enrich_movies.py ../data/box_office_top_50_movies_1995-2014.csv
#       .csv file must have at least columns: movie_id, year, name

import csv
from imdb import IMDb
import pprint
import sys

UPDATE_FILE = True

if len(sys.argv) < 1:
    print "Usage: %s <inputfile>" % sys.argv[0]
    print "       .csv file must have at least columns: movie_id, year, name"
    sys.exit(1)

MOVIE_FILE = sys.argv[1]

ia = IMDb()
movies = []
headers = []
headers_to_add = ['imdb_id', 'imdb_title', 'language', 'country', 'rating']

# Read data from csv
with open(MOVIE_FILE, 'rb') as f:
    rows = csv.reader(f, delimiter=',')
    headers = next(rows, None) # remove header
    # add new headers if not exist
    for h in headers_to_add:
        if h not in headers:
            headers.append(h)
    # populate movies list
    for row in rows:
        movie = {}
        for i, h in enumerate(headers):
            if (i >= len(row)): # doesn't exist, add as blank
                movie[h] = ''
            else:
                movie[h] = row[i]
        movies.append(movie)

def is_int(s):
    try:
        int(s)
        return True
    except ValueError:
        return False

def imdb_key_exists(obj, key):
    try:
        test = obj[key]
        return True
    except KeyError:
        return False

def normalize_title(title):
    return title.lower().replace('.','').replace(':','').replace(',','').replace(' & ',' and ')

def save_movies():
    global MOVIE_FILE
    global headers
    global movies

    with open(MOVIE_FILE, 'wb') as f:
        w = csv.writer(f)
        w.writerow(headers)
        for m in movies:
            row = []
            for h in headers:
                row.append(m[h])
            w.writerow(row)
        # print('Successfully updated file: '+MOVIE_FILE)

def update_movie(mi, movie):
    global movies
    global headers_to_add

    if 'imdb_id' in headers_to_add:
        movies[mi]['imdb_id'] = movie.movieID
    if 'imdb_title' in headers_to_add:
        movies[mi]['imdb_title'] = movie['long imdb canonical title'].encode('utf-8')
    if 'language' in headers_to_add and imdb_key_exists(movie, 'language') and len(movie['language']) > 0:
        movies[mi]['language'] = movie['languages'][0]
    if 'country' in headers_to_add and imdb_key_exists(movie, 'countries') and len(movie['countries']) > 0:
        movies[mi]['country'] = movie['countries'][0]
    if 'rating' in headers_to_add and imdb_key_exists(movie, 'rating'):
        movies[mi]['rating'] = movie['rating']
    # print('Updated: '+movie['long imdb canonical title'])

for mi, m in enumerate(movies):
    # Already processed
    if m['imdb_id']:
        continue
    # Search for movie
    search_string = m['name']+' ('+str(m['year'])+')'
    results = ia.search_movie(search_string)
    found_movie = False
    for ri, r in enumerate(results):
        # Check for year key
        if not imdb_key_exists(r, 'year'):
            ia.update(r)
        if not imdb_key_exists(r, 'year'):
            continue
        # If movie found, save it
        if normalize_title(r['title'])==normalize_title(m['name']) and int(r['year'])==int(m['year']) and r['kind']=='movie' and '"' not in r['long imdb canonical title']:
            found_movie = True
            print('Found match: '+r['long imdb canonical title']+' for '+m['name'])
            movie = r
            ia.update(movie)
            update_movie(mi, movie)
            break
    # If not found
    if not found_movie:
        # Show options
        for ri, r in enumerate(results):
            print(str(ri)+'. '+r['long imdb canonical title']+' ('+r['kind']+', '+str(r.movieID)+')')
        # No results, prompt for entry
        if len(results) <= 0:
            print('No results for: '+m['movie_id']+'. '+m['name']+' ('+m['year']+')')
            selection = raw_input('Your selection for '+m['movie_id']+'. '+m['name']+' ('+m['year']+'): ')
            movie = ia.get_movie(selection)
            if movie:
                print('Found movie: '+movie['long imdb canonical title'])
                update_movie(mi, movie)
        # Save selection
        else:
            selection = raw_input('Your selection for '+m['movie_id']+'. '+m['name']+' ('+m['year']+'): ')
            # User selected result index
            if is_int(selection) and int(selection) < len(results):
                movie = results[int(selection)]
                ia.update(movie)
                update_movie(mi, movie)
            # User manually entered IMDB id
            elif len(selection) > 0 and selection.isdigit():
                movie = ia.get_movie(selection)
                if movie:
                    print('Found movie: '+movie['long imdb canonical title'])
                    update_movie(mi, movie)
                else:
                    print('Could find IMDB id: '+selection)
    if UPDATE_FILE:
        save_movies()
