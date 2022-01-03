from requests import *

fname = input("First Name: ")
sname = input("Second Name: ")

headers = {'X-RapidApi-Key':'9924deea28msh690cfc3273847c8p10ac23jsnc33950a222b5','X-RapidAPI-Host':'love-calculator.p.rapidapi.com'}
r = get('https://love-calculator.p.rapidapi.com/getPercentage?fname='+fname+'&sname='+sname,headers=headers).json()

print(fname + " and " + sname + " have a " + r['percentage'] + "%" + " chance of being together, " + r['result'])