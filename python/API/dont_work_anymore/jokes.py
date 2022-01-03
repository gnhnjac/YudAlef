from requests import *
from time import sleep

choice = input("Programming / Miscellaneous / Dark / Any: ")

headers = {'X-RapidApi-Key':'9924deea28msh690cfc3273847c8p10ac23jsnc33950a222b5','X-RapidAPI-Host':'jokeapi.p.rapidapi.com'}

r = get('https://sv443.net/jokeapi/category/' + choice + '?format=json',headers=headers).json()

if 'joke' in r:
    print(r['joke'])
else:
    print(r['setup'])
    sleep(2)
    print(r['delivery'])
