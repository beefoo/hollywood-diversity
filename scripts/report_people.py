# -*- coding: utf-8 -*-

# Description:
#   Print a report

# Example usage:
#   python report_people.py ../data/people_box_office_top_10_movies_2011-2015_imdb_subset.csv
import csv
import sys

if len(sys.argv) < 1:
    print "Usage: %s <input csv>" % sys.argv[0]
    sys.exit(1)

INPUT_FILE = sys.argv[1]

people = []

# Read people
with open(INPUT_FILE, 'rb') as f:
    r = csv.DictReader(f)
    for row in r:
        people.append(row)

print "%s rows found" % len(people)

no_races = [p for p in people if not p['races']]
print "%s with no races:" % len(no_races)
for p in no_races:
    print p["name"]

no_gender = [p for p in people if not p['gender']]
print "%s with no gender:" % len(no_gender)
for p in no_gender:
    print p["name"]

roles = set([p['role'] for p in people])
for r in roles:
    print "%s with role %s" % (len([p for p in people if p['role']==r]), r)
