# -*- coding: utf-8 -*-

# Example usage:
#   python imdb_get_movie_images.py ../data/box_office_top_10_movies_2011-2015.csv ../tmp/

from bs4 import BeautifulSoup
import csv
import os.path
import re
import sys
import urllib2

if len(sys.argv) < 2:
    print "Usage: %s <inputfile movie csv> <tempdir>" % sys.argv[0]
    sys.exit(1)

MOVIE_FILE = sys.argv[1]
TMP_DIR = sys.argv[2]
overwrite_existing = False
IMDB_URL_PATTERN = 'http://www.imdb.com/title/tt%s/'

movies = []

with open(MOVIE_FILE, 'rb') as f:
    rows = csv.reader(f, delimiter=',')
    headers = next(rows, None) # remove header
    # populate movie list
    for row in rows:
        movie = {}
        for i, h in enumerate(headers):
            movie[h] = row[i]
        movies.append(movie)

print "Attempting to download %s movies..." % len(movies)
for i, m in enumerate(movies):
    url = IMDB_URL_PATTERN % m['imdb_id']
    filename = TMP_DIR + m['imdb_id'] + '.html'
    if overwrite_existing or not os.path.isfile(filename):
        with open(filename,'wb') as f:
            f.write(urllib2.urlopen(url).read())
            f.close()
            print "Downloaded: " + filename

    with open(filename,'rb') as f:
        contents = BeautifulSoup(f, 'html.parser')
        image_src = contents.find('link', rel='image_src')
        if image_src:
            image_url = image_src['href'].replace('630,1200', '808,1200')
            filename = TMP_DIR + m['imdb_id'] + '.jpg'
            if overwrite_existing or not os.path.isfile(filename):
                with open(filename,'wb') as f:
                    f.write(urllib2.urlopen(image_url).read())
                    f.close()
                    print "Downloaded: " + filename
        else:
            print "Could not find image for %s" % m['name']
