# Step 1: Import the necessary required libraries.
import requests
from requests import get
from bs4 import BeautifulSoup
import pandas as pd
import numpy as np

# Step 2: Grab the top 100, sort the result by title.
imdb_url = "https://www.imdb.com/search/title/?groups=top_100&ref_=adv_prv"

# Step 3: Set headers.
headers = {"Accept-Language": "en-US, en;q=0.5"}

# Step 4: Save all values to the results objects coming back from the .get on IMDb URL.
results = requests.get(imdb_url, headers=headers)

# Step 5: Parse the results object to movie_soup using the html parser.
movie_soup = BeautifulSoup(results.text, "html.parser")

# Step 6: I want to extract these attributes (to a list) from the movie_soup.
movie_name = []
movie_years = []
movie_runtime = []
imdb_ratings = []
metascores = []
number_votes = []
us_gross = []

# Step 7: Create a movie_div object to find all div objects in movie_soup.
movie_div = movie_soup.find_all('div', class_='lister-item mode-advanced')

# Step 8: Loop through each object in the movie_div.
for container in movie_div:

# Step 9: Add each result from each attribute for each list.

        # name
        name = container.h3.a.text
        movie_name.append(name)

        # year
        year = container.h3.find('span', class_='lister-item-year').text
        movie_years.append(year)

        # runtime
        runtime = container.p.find('span', class_='runtime').text if container.p.find('span', class_='runtime').text else '-'
        movie_runtime.append(runtime)

        # IMDB rating
        imdb = float(container.strong.text)
        imdb_ratings.append(imdb)

        # metascore
        m_score = container.find('span', class_='metascore').text if container.find('span', class_='metascore') else '-'
        metascores.append(m_score)

        # There are two NV containers, grab both of them as they hold both the votes and the grosses
        nv = container.find_all('span', attrs={'name': 'nv'})

        # filter nv for votes
        vote = nv[0].text
        number_votes.append(vote)

        # filter nv for gross
        grosses = nv[1].text if len(nv) > 1 else '-'
        us_gross.append(grosses)

# Step 10: Build and store all of the attributes into the Pandas movie dataframe.
movies = pd.DataFrame({
'movie_name': movie_name,
'movie_year': movie_years,
'movie_runtime': movie_runtime,
'imdb_ratings': imdb_ratings,
'metascore': metascores,
'number_votes': number_votes,
'us_gross_millions': us_gross,
})

# Step 11: Use Pandas str.extract to remove all String characters, and save the value as type int for cleaning up the data with Pandas.
movies['movie_year'] = movies['movie_year'].str.extract('(\d+)').astype(int)
movies['movie_runtime'] = movies['movie_runtime'].str.extract('(\d+)').astype(int)
movies['metascore'] = movies['metascore'].astype(int)
movies['number_votes'] = movies['number_votes'].str.replace(',', '').astype(int)
movies['us_gross_millions'] = movies['us_gross_millions'].map(lambda x: x.lstrip('$').rstrip('M'))
movies['us_gross_millions'] = pd.to_numeric(movies['us_gross_millions'], errors='coerce')

# Step 12: Export our movie results to a pretty little .csv file.
movies.to_csv('top_100_movies.csv')