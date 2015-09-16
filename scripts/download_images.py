# -*- coding: utf-8 -*-

# Example usage:
#   python download_images.py ../data/people_box_office_top_50_movies_1995-2014_imdb_subset.csv ../tmp/

import csv
import os.path
import sys
import urllib2

if len(sys.argv) < 2:
    print "Usage: %s <inputfile people csv> <outputdir>" % sys.argv[0]
    print "       people csv file must contain at least columns: imdb_id, img"
    sys.exit(1)

INPUT_FILE = sys.argv[1]
OUTPUT_DIR = sys.argv[2]
overwrite_existing = False

people = []
filename_col = 'imdb_id'
required_cols = ['imdb_id', 'img']

with open(INPUT_FILE, 'rb') as f:
    rows = csv.reader(f, delimiter=',')
    headers = next(rows, None) # remove header
    for col in required_cols:
        if col not in headers:
            print "People csv file must contain at least columns: imdb_id, img"
            sys.exit(1)
    # populate people list
    for row in rows:
        person = {}
        for i, h in enumerate(headers):
            if h in required_cols:
                person[h] = row[i]
        people.append(person)

# Find unique people
people = {p['imdb_id']:p for p in people}.values()

# Filter out invalid images
people = [p for p in people if p['img'] and p['img']!='none']

print "Attempting to download " + str(len(people)) + " images..."

# Download images
for p in people:
    extension = p['img'].split('.')[-1]
    filename = OUTPUT_DIR + p[filename_col] + '.' + extension
    if overwrite_existing or not os.path.isfile(filename):
        with open(filename,'wb') as f:
            f.write(urllib2.urlopen(p['img']).read())
            f.close()
            print "Downloaded " + p['img']
