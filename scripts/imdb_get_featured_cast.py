# -*- coding: utf-8 -*-

# Example usage:
#   python imdb_get_featured_cast.py ../data/box_office_top_10_movies_2011-2015.csv ../data/people_box_office_top_10_movies_2011-2015_imdb_subset.csv ../tmp/

from bs4 import BeautifulSoup
import csv
import os.path
import re
import sys
import urllib2

if len(sys.argv) < 3:
    print "Usage: %s <inputfile movie csv> <inputfile people csv> <tempdir>" % sys.argv[0]
    sys.exit(1)

MOVIE_FILE = sys.argv[1]
PEOPLE_FILE = sys.argv[2]
TMP_DIR = sys.argv[3]
overwrite_existing = False

movies = []
people = []

IMDB_URL_PATTERN = 'http://www.imdb.com/title/tt%s/'
ACTOR_URL_PATTERN = '\/name\/nm[0]*([1-9][0-9]+)\/\?ref\_\=[a-z0-9\_]+'

with open(MOVIE_FILE, 'rb') as f:
    rows = csv.reader(f, delimiter=',')
    headers = next(rows, None) # remove header
    # populate movie list
    for row in rows:
        movie = {}
        for i, h in enumerate(headers):
            movie[h] = row[i]
        movies.append(movie)

with open(PEOPLE_FILE, 'rb') as f:
    rows = csv.reader(f, delimiter=',')
    headers = next(rows, None) # remove header
    # populate people list
    for row in rows:
        person = {}
        for i, h in enumerate(headers):
            person[h] = row[i]
        people.append(person)

print "Attempting to download %s movies..." % len(movies)
for i, m in enumerate(movies):
    featured = []
    url = IMDB_URL_PATTERN % m['imdb_id']
    filename = TMP_DIR + m['imdb_id'] + '.html'
    if overwrite_existing or not os.path.isfile(filename):
        with open(filename,'wb') as f:
            f.write(urllib2.urlopen(url).read())
            f.close()
            print "Downloaded: " + filename

    with open(filename,'rb') as f:
        contents = BeautifulSoup(f, 'html.parser')
        actor_container = contents.find('div', itemprop='actors')
        actor_links = actor_container.findAll('a', itemprop='url')
        for actor_link in actor_links:
            # Find the name
            name = ""
            name_span = actor_link.find('span', itemprop='name')
            if name_span:
                name = name_span.string

            # Find the imdb id
            actor_url = actor_link['href']
            imdb_id = ""
            match = re.search(ACTOR_URL_PATTERN, actor_url)
            if match:
                imdb_id = match.group(1)
                featured.append({
                    "name": name,
                    "imdb_id": imdb_id
                })
                # print "Found IMDB ID for %s in movie %s" % (name, m['name'])
            elif name:
                print "Could not find IMDB ID for %s in movie %s (%s)" % (name, m['name'], m['imdb_id'])

    cast = [p for p in people if p['movie_id']==m['movie_id']]
    cast_ids = [p['imdb_id'] for p in cast]
    missing = [p for p in featured if p['imdb_id'] not in cast_ids]
    if len(missing) > 0:
        print "Missing: %s from %s" % (', '.join([p['name'] + ' (' +p['imdb_id']+ ')' for p in missing]), m['name'])
