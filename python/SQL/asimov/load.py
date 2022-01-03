import sqlite3
import requests
import re
from bs4 import BeautifulSoup

db = sqlite3.connect("asimov.db")

sql = db.cursor()

res = requests.get("http://www.asimovonline.com/oldsite/asimov_titles.html")

soup = BeautifulSoup(res.content)

pres = soup.findAll('pre')

a_elements = soup.findAll('a')

for a in a_elements:
    a.extract()

book_str = ""
for e in pres:

    book_str += e.text

book_list = book_str.split('\n')

del book_list[0]
del book_list[0]

for i, e in enumerate(book_list):

    book_list[i] = re.split(r'\s{2,}', e)

    e_list = book_list[i]

    if len(e_list) == 5:
        del e_list[0]
    elif len(e_list) == 4:
        print("EYY")
        del e_list[0]
        book_list[i-1][1] += e_list[0]
        book_list[i-1].append(e_list[1])
        book_list[i-1].append(e_list[2])

    print(e_list, i)