# -*- coding: utf-8 -*-

# Example usage:
#   python imdb_get_characters.py ../data/cast_box_office_top_10_movies_2006-2015_imdb.csv  ../tmp/html/

from bs4 import BeautifulSoup
import csv
import os.path
import re
import sys
import urllib2

if len(sys.argv) < 3:
    print "Usage: %s <inputfile people csv> <tempdir>" % sys.argv[0]
    sys.exit(1)

PEOPLE_FILE = sys.argv[1]
TMP_DIR = sys.argv[2]

column_name = 'role'
people = []
headers = []

IMDB_URL_PATTERN = 'http://www.imdb.com/title/tt%s/fullcredits'
ACTOR_URL_PATTERN = '\/name\/nm[0]*([1-9][0-9]+)\/\?ref\_\=[a-z0-9\_]+'

with open(PEOPLE_FILE, 'rb') as f:
    rows = csv.reader(f, delimiter=',')
    headers = next(rows, None) # remove header
    if column_name not in headers:
        headers.append(column_name)
    # populate people list
    for row in rows:
        person = {}
        for i, h in enumerate(headers):
            if i >= len(row):
                person[h] = ''
            else:
                person[h] = row[i]
        people.append(person)

def saveFile():
    global PEOPLE_FILE
    global headers
    global people

    with open(PEOPLE_FILE, 'wb') as f:
        w = csv.writer(f)
        w.writerow(headers)
        for p in people:
            row = []
            for h in headers:
                row.append(p[h])
            w.writerow(row)
        print "Updated file %s" % PEOPLE_FILE

print "Attempting to download html files..."
for i, p in enumerate(people):
    if p[column_name]:
        continue
    url = IMDB_URL_PATTERN % p['movie_imdb_id']
    filename = TMP_DIR + p['movie_imdb_id'] + '_fullcredits.html'
    if not os.path.isfile(filename):
        with open(filename,'wb') as f:
            f.write(urllib2.urlopen(url).read())
            f.close()
            print "Downloaded: " + filename

    with open(filename,'rb') as f:
        contents = BeautifulSoup(f, 'html.parser')
        cast_list_container = contents.find('table', 'cast_list')
        if not cast_list_container:
            print "No cast list for %s" % filename
            continue
        rows = cast_list_container.findAll('tr', re.compile("even|odd"))
        found = False

        for row in rows:
            actor_container = row.find('td', itemprop="actor")
            character_container = row.find('td', "character")
            character_container = character_container.find('div')
            character_link = character_container.find('a')
            if character_link:
                character = character_link.string
            else:
                character = character_container.string
            character = re.sub('\s+', ' ', character).strip()

            actor_link = actor_container.find('a', itemprop="url")
            if actor_link:
                actor_url = actor_link['href']
                match = re.search(ACTOR_URL_PATTERN, actor_url)
                if match:
                    imdb_id = match.group(1)
                    if imdb_id == p['imdb_id']:
                        people[i][column_name] = character.encode('utf-8')
                        found = True
                        break

        if not found:
            print "Found no match for %s in %s" % (p["name"], p["movie_name"])
        else:
            saveFile()
