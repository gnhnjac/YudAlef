import requests
from requests import *

def main():
    base_url = 'https://www.reddit.com/'
    data = {'grant_type': 'password', 'username': 'gnhnjac', 'password': 'Kraizel18112004'}
    auth = requests.auth.HTTPBasicAuth('oofmvPMEj8qsQQ', 'EYQ3RNq3YfggJaUnF5K2xN8qUQM')
    r = requests.post(base_url + 'api/v1/access_token',
                      data=data,
                      headers={'user-agent': 'APP-NAME by REDDIT-USERNAME'},
              auth=auth)
    d = r.json()

    token = 'bearer ' + d['access_token']

    global SameAsBefore
    if not SameAsBefore:

        global subreddit
        subreddit = input("Which subreddit? ")

    headers = {'Authorization': token, 'User-Agent': 'Reddit Api by gnhnjac'}

    params = {'query': subreddit}

    subreddit_name = get('https://oauth.reddit.com/api/search_reddit_names', headers=headers, params=params).json()

    response = get(f'https://oauth.reddit.com/r/{subreddit_name["names"][0]}/random', headers=headers).json()

    root = response[0]['data']['children'][0]['data']

    text = root['selftext']

    if text == '':
        text = 'no text in body,\n' + root['url']

    else:

        text_list = list(text)
        index = 0
        for letter in text_list:

            if letter in ('.', ',', '!', '?', ';'):
                letter += '\n'
                text_list[index] = letter
            index += 1
        text = ''.join(text_list)

    print(f'{root["title"]} \n\n {text}')

    choice = input("Again? ")

    if 'yes' in choice.lower():
        if 'b' in choice.lower():
            SameAsBefore = True
            subreddit = subreddit
        else:
            SameAsBefore = False
        main()

SameAsBefore = False
main()