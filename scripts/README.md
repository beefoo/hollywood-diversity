# Hollywood Diversity Scripts

These are a set of scripts for retrieving, processing, and enriching data about movies and the people associated with those movies using IMDB.  Here are the steps I used:

1. Start with a [.csv file](https://github.com/beefoo/hollywood-diversity/blob/master/data/box_office_top_50_movies_1995-2014.csv) of movies to look up on IMDB. This particular list contains the top 50 domestic (U.S.) movies by Total Gross ($) from 1995 to 2014. However for these set of scripts, this file could contain any list of movies. Required columns are: movie_id, year, name.
2. Run the [imdb_enrich_movies.py](https://github.com/beefoo/hollywood-diversity/blob/master/scripts/imdb_enrich_movies.py) script on the above file which adds IMDB information to it and prompts the user if there are any ambiguities.
   
   ```
   python imdb_enrich_movies.py ../data/box_office_top_50_movies_1995-2014.csv
   ```
   
3. Run the [imdb_get_people.py](https://github.com/beefoo/hollywood-diversity/blob/master/scripts/imdb_get_people.py) script which retrieves people involved in those movies from IMDB.
   ```
   python imdb_get_people.py ../data/box_office_top_50_movies_1995-2014.csv ../data/people_box_office_top_50_movies_1995-2014_imdb.csv
   ```
4. Run the [imdb_get_images.py](https://github.com/beefoo/hollywood-diversity/blob/master/scripts/imdb_get_images.py) script which attempts to retrieve the images of the people by scraping their IMDB page
   
   ```
   python imdb_get_images.py ../data/people_box_office_top_50_movies_1995-2014_imdb.csv
   ```
   
5. (optional) Run the [guess_gender_race.py](https://github.com/beefoo/hollywood-diversity/blob/master/scripts/guess_gender_race.py) script which attempts to populate columns "gender" and "race" based on "name" in csv using name data from the U.S. Census Bureau and the Social Security Administration.
   
   ```
   python guess_gender_race.py ../data/people_box_office_top_50_movies_1995-2014_imdb.csv
   ```
   
6. (optional) Run the [filter_people.py](https://github.com/beefoo/hollywood-diversity/blob/master/scripts/filter_people.py) script which limits the number of people per movie based on their role
   
   ```
   python filter_people.py ../data/people_box_office_top_50_movies_1995-2014_imdb.csv ../data/people_box_office_top_50_movies_1995-2014_imdb_subset.csv
   ```
   
7. Run the [generate_json.py](https://github.com/beefoo/hollywood-diversity/blob/master/scripts/generate_json.py) script which generates json files for movies, people, and roles.
   
   ```
   python generate_json.py ../data/box_office_top_50_movies_1995-2014.csv ../data/people_box_office_top_50_movies_1995-2014_imdb_subset.csv
   ```
