# -*- coding: utf-8 -*-

import csv
import os

INPUT_FILE = '../data/people_box_office_top_50_movies_1995-2014.csv'
UPDATE_FILE = True

people_movie_roles = []
headers = []
missing = []
errors = []

def valid_name(s):
    return (s[0].isalpha() or s[-1].isalpha()) and not '=' in s

# Read data from csv
with open(INPUT_FILE, 'rb') as f:
    r = csv.reader(f, delimiter=',')
    headers = next(r, None) # remove header
    for movie_id, movie_name, movie_url, role, name, url, gender, race in r:
        if not name:
            print('Missing name in '+movie_id+'-'+movie_name)

        elif valid_name(name):
            people_movie_roles.append({
                'index': len(people_movie_roles),
                'movie_id': int(movie_id),
                'movie_name': movie_name,
                'movie_url': movie_url,
                'role': role,
                'name': name,
                'url': url,
                'gender': gender,
                'race': race
            })

        else:
            print('Invalid name '+name+' in '+movie_id+'-'+movie_name)

# Update URLs
no_urls = [p for p in people_movie_roles if not p['url']]
updated_urls = 0
for p in no_urls:
    matches = [pp['url'] for pp in people_movie_roles if pp['name']==p['name'] and pp['url']]
    if len(matches) > 0:
        people_movie_roles[p['index']]['url'] = matches[0]
        # print('Found '+people_movie_roles[p['index']]['name']+' URL: '+matches[0])
        updated_urls += 1
print('Found '+str(updated_urls)+ ' URLs for names')

# Update names based on URLs
urls = set([p['url'] for p in people_movie_roles if p['url']])
for url in urls:
    names = set([p['name'] for p in people_movie_roles if p['url']==url])
    if len(names) > 1:
        print('Found discrepancy: '+names.join(', '))

# Write data back to file
if UPDATE_FILE:
    with open(INPUT_FILE, 'wb') as f:
        w = csv.writer(f)
        w.writerow(headers)
        for p in people_movie_roles:
            row = []
            for h in headers:
                row.append(p[h])
            w.writerow(row)
        print('Successfully updated file: '+INPUT_FILE)
