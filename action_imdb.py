from bs4 import BeautifulSoup
import requests
import pandas as pd
import sqlite3

try:
    response = requests.get(
        "https://www.imdb.com/search/title/?genres=action&sort=user_rating,desc&title_type=feature&num_votes=25000,&pf_rd_m=A2FGELUUNOQJNL&pf_rd_p=94365f40-17a1-4450-9ea8-01159990ef7f&pf_rd_r=YSFKH48A74Y37XYV8BZG&pf_rd_s=right-6&pf_rd_t=15506&pf_rd_i=top&ref_=chttp_gnr_1")
    soup = BeautifulSoup(response.text, 'html.parser')
    # print(soup)
    movies = soup.find('div', class_="lister-list").find_all("div", class_="lister-item")
    movie_list = {"movie_index": [], "movie_name": [], "movie_year": [], "movie_rate": [], "movie_director": [], "movie_story": [], "movie_gross": []}

    for movie in movies:
        # print(movie)
        index = movie.find('h3').find('span', class_="lister-item-index").get_text().split('.')[0]
        movie_name = movie.find('h3', class_="lister-item-header").a.text
        year = movie.find('h3').find('span', class_="lister-item-year").get_text().replace('(', " ")
        year = year.replace(')', " ")
        rate = movie.find("div", class_="ratings-imdb-rating").strong.text
        director = movie.find('p', class_="").a.text

        story = movie.find('p').findNext('p').get_text()
        gross = movie.find('p', class_="sort-num_votes-visible").find_all('span')[-1].get_text()
        # print(index,movie_name,year,rate,director,story,gross)

        movie_list["movie_index"].append(index)
        movie_list["movie_name"].append(movie_name)
        movie_list["movie_year"].append(year)
        movie_list["movie_rate"].append(rate)
        movie_list["movie_director"].append(director)
        movie_list["movie_story"].append(story)
        movie_list["movie_gross"].append(gross)


except Exception as e:
    print(e)

df = pd.DataFrame(data=movie_list)
print(df.head())

connection = sqlite3.connect("Top 50 Action Movies.db")
cursor = connection.cursor()

qry = "CREATE TABLE IF NOT EXISTS action(movie_index,movie_name,movie_year,movie_rate,movie_director,movie_story,movie_gross)"
cursor.execute(qry)

for i in range(len(df)):
    cursor.execute("insert into action values(?,?,?,?,?,?,?)", df.iloc[i])

connection.commit()
connection.close()







