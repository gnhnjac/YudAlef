from requests import *

def rand(min, max):

    params = {"jsonrpc": "2.0","id": 42,"method":"generateIntegers","params":{"apiKey":"9433a55c-6b6c-45b8-8ab8-ee046cee8eb5","n":1,"min":min,"max":max}}
    r = post("https://api.random.org/json-rpc/2/invoke", json=params).json()

    return r['result']['random']['data'][0]