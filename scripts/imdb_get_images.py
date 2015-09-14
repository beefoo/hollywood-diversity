# -*- coding: utf-8 -*-

# Description:
#   This file takes in a .csv file of people and retrieves their images from IMDB if they exist

# Example usage:
#   python imdb_get_images.py ../data/people_box_office_top_50_movies_1995-2014_imdb.csv

from bs4 import BeautifulSoup
import csv
import sys
import urllib2

if len(sys.argv) < 1:
    print "Usage: %s <inputfile csv>" % sys.argv[0]
    sys.exit(1)

PEOPLE_FILE = sys.argv[1]
overwrite_existing = False
update_file = True

images = {}
people = []
headers = []
headers_to_add = ['img']

with open(PEOPLE_FILE, 'rb') as f:
    rows = csv.reader(f, delimiter=',')
    headers = next(rows, None) # remove header
    if 'imdb_id' not in headers:
        print PEOPLE_FILE + " must have column <imdb_id>"
        sys.exit(1)
    # init people list
    for h in headers_to_add:
        if h not in headers:
            headers.append(h)
    # populate people list
    for row in rows:
        person = {}
        for i, h in enumerate(headers):
            if (i >= len(row)): # doesn't exist, add as blank
                person[h] = ''
            else:
                person[h] = row[i]
        people.append(person)

for i, p in enumerate(people):
    # Image was already found for this person
    if p['imdb_id'] in images:
        people[i]['img'] = images[p['imdb_id']]
    # Otherwise, fetch remote page and parse for image
    elif overwrite_existing or not p['img']:
        html_contents = urllib2.urlopen("http://akas.imdb.com/name/nm"+p['imdb_id']+"/").read()
        contents = BeautifulSoup(html_contents, 'html.parser')
        image_srcs = contents.findAll('link', rel='image_src')
        image_src = 'none'
        # image found
        if len(image_srcs):
            image_src = image_srcs[0]['href']
        # image is default image
        if 'imdb_fb_logo' in image_src:
            image_src = 'none'
        people[i]['img'] = image_src
        images[p['imdb_id']] = image_src
        print 'Found ' + people[i]['img'] + ' for '+p['imdb_id']

# Write data back to file
if update_file:
    with open(PEOPLE_FILE, 'wb') as f:
        w = csv.writer(f)
        w.writerow(headers)
        for p in people:
            row = []
            for h in headers:
                row.append(p[h])
            w.writerow(row)
        print('Successfully updated file: '+PEOPLE_FILE)
