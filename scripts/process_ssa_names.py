# -*- coding: utf-8 -*-

# Download files from http://www.ssa.gov/oact/babynames/limits.html
# And place .txt files in input directory

import csv
import glob

INPUT_DIR = "../data/ssa_names/"
OUTPUT_FILE = "../data/firstnames.csv"
START_YEAR = 1920
END_YEAR = 2000

names = []

# Go through directory
for filepath in glob.glob(INPUT_DIR + "yob*.txt"):
    # check if year is valid
    filename = filepath.split('/')[-1]
    year = int(filename[3:7])
    if year < START_YEAR or year > END_YEAR:
        continue
    print('Processing '+str(year)+'...')
    # open file as csv
    with open(filepath, 'rb') as f:
        r = csv.reader(f, delimiter=',')
        for name, gender, count in r:
            # if name already exists, update count as average of two
            matches = [n for n in names if n['name']==name.lower() and n['gender']==gender.lower()]
            if len(matches) > 0:
                match = matches[0]
                names[match['index']]['count'] = round(0.5*(match['count']+int(count)))
            # otherwise, add it
            else:
                names.append({
                    'index': len(names),
                    'name': name.lower(),
                    'gender': gender.lower(),
                    'count': int(count)
                })

# sort by count, desc
names = sorted(names, key=lambda k: k['count'], reverse=True)

# output as csv
with open(OUTPUT_FILE, 'wb') as f:
    w = csv.writer(f)
    for n in names:
        w.writerow([n['name'], n['gender']])
    print('Successfully wrote '+str(len(names))+' names to file: '+OUTPUT_FILE)
