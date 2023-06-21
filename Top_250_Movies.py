from bs4 import BeautifulSoup
import requests, openpyxl
#import pandas as pd                       \\Remove the Hashtag and Remove openpyxl to get a database file.
#import sqlite3

excel=openpyxl.Workbook()
sheet=excel.active
sheet.title="Top 250 movies"
sheet.append(['Rank','Movie Name','Year of Release','IMDB Rating'])

try:
    response = requests.get("https://www.imdb.com/chart/top/")
    soup = BeautifulSoup(response.text, 'html.parser')
    # print(soup)
    movies = soup.find('tbody', class_="lister-list").find_all("tr")
    #movie_list = {"movie_rank": [], "movie_name": [], "movie_year": [], "movie_rate": []}

    for movie in movies:
        # print(movie)
        rank = movie.find('td', class_="titleColumn").get_text(strip=True).split('.')[0]
        movie_name = movie.find('td', class_="titleColumn").a.text
        rate = movie.find('td', class_="ratingColumn").strong.text
        year = movie.find('td', class_="titleColumn").span.text.replace('(', " ")
        year = year.replace(')', " ")

        # print(rank,movie_name,rate,year)
        #movie_list["movie_rank"].append(rank)
        #movie_list["movie_name"].append(movie_name)
        #movie_list["movie_year"].append(year)
        #movie_list["movie_rate"].append(rate)

        sheet.append([rank,movie_name,year,rate])


except Exception as e:
    print(e)

excel.save("Top 250 Movies in IMDB.xlsx")


#df = pd.DataFrame(data=movie_list)
#print(df.head())

#connection = sqlite3.connect("Top 250 Movies.db")
#cursor = connection.cursor()

#qry = "CREATE TABLE IF NOT EXISTS movies(movie_rank,movie_name,movie_year,movie_rate)"
#cursor.execute(qry)

#for i in range(len(df)):
    #cursor.execute("insert into movies values(?,?,?,?)", df.iloc[i])

#connection.commit()
#connection.close()






