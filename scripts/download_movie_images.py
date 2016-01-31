# -*- coding: utf-8 -*-

# Example usage:
#   python download_movie_images.py ../data/cast_box_office_top_10_movies_2006-2015_imdb.csv ../tmp/

import csv
import os.path
import sys
import urllib2,cookielib

if len(sys.argv) < 2:
    print "Usage: %s <inputfile people csv> <outputdir>" % sys.argv[0]
    print "       people csv file must contain at least columns: movie_imdb_id, imdb_id, img_movie"
    sys.exit(1)

INPUT_FILE = sys.argv[1]
OUTPUT_DIR = sys.argv[2]
overwrite_existing = False

people = []
required_cols = ['movie_imdb_id', 'imdb_id', 'img_movie']

hdr = {'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.11 (KHTML, like Gecko) Chrome/23.0.1271.64 Safari/537.11',
       'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
       'Accept-Charset': 'ISO-8859-1,utf-8;q=0.7,*;q=0.3',
       'Accept-Encoding': 'none',
       'Accept-Language': 'en-US,en;q=0.8',
       'Connection': 'keep-alive'}

with open(INPUT_FILE, 'rb') as f:
    rows = csv.reader(f, delimiter=',')
    headers = next(rows, None) # remove header
    for col in required_cols:
        if col not in headers:
            print "People csv file must contain at least columns: %s" % ",".join(required_cols)
            sys.exit(1)
    # populate people list
    for row in rows:
        person = {}
        for i, h in enumerate(headers):
            if h in required_cols:
                person[h] = row[i]
        people.append(person)

# Filter out invalid images
people = [p for p in people if p['img_movie']]

print "Attempting to download " + str(len(people)) + " images..."

# Download images
downloaded = 0
errors = 0
for p in people:
    extension = 'jpg'
    if not p['img_movie']:
        continue
    if '.png' in p['img_movie'] and '.jpg' not in p['img_movie']:
        extension = 'png'
    filename = OUTPUT_DIR + p['imdb_id'] + '_' + p['movie_imdb_id'] + '.' + extension
    if overwrite_existing or not os.path.isfile(filename):
        print "Downloading " + p['img_movie']
        contents = False
        req = urllib2.Request(p['img_movie'], headers=hdr)
        try:
           contents = urllib2.urlopen(req).read()
        except urllib2.HTTPError, err:
           print err.reason + " (" +p['img_movie']+ ")"
           errors += 1
        if contents:
            with open(filename,'wb') as f:
                f.write(contents)
                f.close()
                print "  Downloaded " + p['img_movie']
                downloaded += 1


print "Downloaded %s images" % downloaded
print "Errors %s images" % errors
print "Skipped % s images" % (len(people)-downloaded-errors)
