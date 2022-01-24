from requests import *

headers = {'X-RapidApi-Key': '9924deea28msh690cfc3273847c8p10ac23jsnc33950a222b5',
           'X-RapidAPI-Host': 'community-open-weather-map.p.rapidapi.com'}

region = input("Where? ")

r = get(f'https://community-open-weather-map.p.rapidapi.com/weather?q={region}', headers=headers).json()

print(f'Region: {r["name"]}\n'
      f'Degrees: {round(r["main"]["temp"]-273.15)}°C\n'
      f'Description: {r["weather"][0]["description"]}')
