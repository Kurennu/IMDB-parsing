from bs4 import BeautifulSoup
import requests
import pandas as pd

url = "https://www.imdb.com/chart/top?sort=ir,desc&mode=simple&page=1"
page = requests.get(url)
text = page.text
soup = BeautifulSoup(text, "lxml")

table = soup.find('table')

titles = []  # Название фильма
authors = [] # Режиссеры и авторы
year = []    # Год выпуска
rating = []  # Рейтинг IMDb

for item in table.find_all('a'):
    titles.append(item.text.strip())
    authors.append(item.get('title'))

titles = list(filter(None, titles))
authors = list(filter(None, authors))

for item in table.find_all('span', {"class" : "secondaryInfo"}):
    year.append(item.text)

year = [int(i[1:5]) for i in year]

for item in table.find_all('strong'):
    rating.append(item.text)

top = [int(i) for i in range(1, 251)]

df = pd.DataFrame({'ТОП': top, 'Название фильма': titles, 'Режиссёр и автор сценария': authors,
                   'Год выпуска': year, 'Рейтинг IMDb': rating})
df = df.set_index('ТОП')
print(df)
