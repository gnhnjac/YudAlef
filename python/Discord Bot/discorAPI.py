
import discord
from random import randint as rnd
from discord.ext import commands
import asyncio
from PIL import ImageGrab
import random
from pyautogui import *
from time import sleep
from gtts import gTTS
from os import listdir
import youtube_dl
import requests

client = commands.Bot(command_prefix='.')


@client.event
async def on_ready():
    print(f"Logged In: {client.user}")
    await client.change_presence(activity=discord.Game('with your mom'))


@client.event
async def on_message(message):
    print(f'{message.guild}: {message.channel}: {message.author}: {message.author.name}: {message.content}')

    if "bulbul" in message.content.lower() and message.author.name != 'Aba Karir 69':
        meslist = message.content.split(" ")

        bulbulind = meslist.index('bulbul')

        meslist[bulbulind] = "**bulbul**"

        final = " ".join(meslist)

        await message.channel.send(final)
    await client.process_commands(message)


@client.command()
async def vcexit(ctx):
    await vc.disconnect()

@client.command()
async def fart(ctx):
    channel = ctx.message.author.voice.channel
    global vc
    vc = await channel.connect()
    vc.play(discord.FFmpegPCMAudio("Fart.mp3"), after=lambda e: print('done', e))
    while vc.is_playing():
        await asyncio.sleep(1)
    await vc.disconnect()

@client.command()
async def vcvol(ctx, *, vols):
    vol = int(vols)/100
    vc.source = discord.PCMVolumeTransformer(vc.source)
    vc.source.volume = vol
    await ctx.send(f':speaker: ``Volume changed to:`` ``{vols}`` :speaker:')

@client.command()
async def skip(ctx):
    vc.stop()

@client.command()
async def stop(ctx):
    global break_var
    break_var = True


def download_song(song_url, song_title):
    """
    Download a song using youtube url and song title
    """

    outtmpl = song_title + '.%(ext)s'
    ydl_opts = {
        'format': 'bestaudio/best',
        'outtmpl': outtmpl,
        'postprocessors': [
            {'key': 'FFmpegExtractAudio','preferredcodec': 'mp3',
             'preferredquality': '192',
            },
            {'key': 'FFmpegMetadata'},
        ],
    }

    with youtube_dl.YoutubeDL(ydl_opts) as ydl:

        info_dict = ydl.download([song_url])


songqueue = []


def ytplay(message):
    if 'https://www.youtube.com/watch?' in message and '&list=' in message:

        _, playlist_id = message.split('list=', 1)

        params = {'part': 'snippet', 'maxResults': '50',
                  'playlistId': playlist_id,
                  'key': 'AIzaSyDEGpg_0o68G07FfWdqq_vNwxNcpiGEXrg'}

        get = requests.get('https://www.googleapis.com/youtube/v3/playlistItems', params=params).json()

        for playlist_item in get['items']:
            global video_id
            video_id = playlist_item['snippet']['resourceId']['videoId']
            global videoname
            videoname = playlist_item['snippet']['title']

            queue.append(videoname + '\n')

            global songqueue
            songqueue.append(f'https://www.youtube.com/watch?v={video_id}')

        params = {'part': 'snippet', 'id': playlist_id,
                  'key': 'AIzaSyDEGpg_0o68G07FfWdqq_vNwxNcpiGEXrg'}

        get = requests.get('https://www.googleapis.com/youtube/v3/playlists', params=params).json()

        playlist_name = get['items'][0]['snippet']['title']

        return playlist_name

    else:
        params = {'part': 'snippet', 'q': message, 'key': 'AIzaSyDEGpg_0o68G07FfWdqq_vNwxNcpiGEXrg'}

        get = requests.get('https://www.googleapis.com/youtube/v3/search', params=params).json()

        for id in get['items']:
            if 'videoId' in id['id']:
                video_id = id['id']['videoId']
                videoname = id['snippet']['title']
                break

        queue.append(videoname + '\n')

        songqueue.append(f'https://www.youtube.com/watch?v={video_id}')

        return videoname

@client.command()
async def yt(ctx, *, message):

    global songqueue
    if songqueue == []:
        global queue
        queue = []

        channel = ctx.message.author.voice.channel
        global vc
        vc = await channel.connect()

        await ctx.send(f'{ytplay(message)} added to queue!')

        a = await ctx.send(":speaker: ``Now Playing: `` :speaker:")
        await a.add_reaction(emoji='⏹')
        await a.add_reaction(emoji='⏸')
        await a.add_reaction(emoji='⏩')

        global break_var
        break_var = False
        booted_up = False

        while songqueue:

            if break_var:
                songqueue = []
                queue = []
                break

            await a.edit(content=f":speaker: ``Now Playing: {queue[0]}`` :speaker:")

            print(songqueue[0])

            download_song(songqueue[0], 'song')
            vc.play(discord.FFmpegPCMAudio("song.mp3"), after=lambda e: print('done', e))

            while vc.is_playing():

                a = await a.channel.fetch_message(a.id)
                countstop = a.reactions[0].count
                countpause = a.reactions[1].count
                countskip = a.reactions[2].count

                if countskip == 2:
                    await a.remove_reaction('⏩', reauser)
                    vc.stop()

                if countpause == 2:
                    vc.pause()
                    while countpause > 1:
                        if countpause == 3:
                            await a.remove_reaction('⏸', reauser)
                        message = await a.channel.fetch_message(a.id)
                        countpause = message.reactions[1].count
                    vc.resume()

                if countstop == 2 or break_var:
                    break_var = True
                    vc.stop()
                    break

                await asyncio.sleep(1)

            songqueue.remove(songqueue[0])
            queue.remove(queue[0])
        await vc.disconnect()
        queue = []
    else:

        await ctx.send(f'{ytplay(message)} added to queue!')


@client.command()
async def queue(ctx):

    if queue:
        if 'Now Playing: ' not in queue[0]:
            queue[0] = 'Now Playing: ' + queue[0] + '\n\n'

    await ctx.send(f'```{"".join(queue)}```')


@client.command()
async def tts(ctx, *, voiceline):
    tts = gTTS(text=voiceline, lang='en')
    tts.save("tts.mp3")

    channel = ctx.message.author.voice.channel
    global vc
    vc = await channel.connect()
    vc.play(discord.FFmpegPCMAudio("tts.mp3"), after=lambda e: print('done', e))
    while vc.is_playing():
        await asyncio.sleep(1)
    await vc.disconnect()


@client.command()
async def bruh(ctx):
    message = ctx.message.content
    if " " in message:
        bruhd = message.replace(".bruh ", '')
        await ctx.send(f":fire: ``{bruhd} got BRUH'D``:fire: ")
    else:
        ms = await ctx.send(f":fire: ``{ctx.message.author.name} got BRUH'D``:fire: ")
    channel = ctx.message.author.voice.channel
    vc = await channel.connect()
    if " " in message:
        boy = bruhd
    else:
        boy = ctx.message.author.name
    tts = gTTS(text=boy + ",", lang='en')
    tts.save("bruhtts.mp3")
    vc.play(discord.FFmpegPCMAudio("bruhtts.mp3"), after=lambda e: print('done', e))
    while vc.is_playing():
        await asyncio.sleep(1)
    vc.play(discord.FFmpegPCMAudio("bruh.mp3"), after=lambda e: print('done', e))
    while vc.is_playing():
        await asyncio.sleep(1)
    await vc.disconnect()


@client.command()
async def cumrace(ctx, *, y):
    await ctx.message.add_reaction(emoji='🍆')
    x = 1
    stroke = [':punch::skin-tone-5:', '=', '=', '=']
    highest = list()
    contestants = list()
    winners = list()
    if int(y) > 100:
        await ctx.send('Too many contestants')
    else:
        while x <= int(y):
            rndcum = rnd(0, 69)

            highest.append(rndcum)

            contestants.append(str(x)+':'+str(rndcum))
            await ctx.send(f"{x}: 8{''.join(stroke)}[}} " + '- ' * rndcum)
            x += 1

            fistind = stroke.index(':punch::skin-tone-5:')
            if fistind == 0:
                up = True
            if fistind == 3:
                up = False
            if up:
                stroke[fistind] = '='
                stroke[fistind+1] = ':punch::skin-tone-5:'
            if not up:
                stroke[fistind] = '='
                stroke[fistind - 1] = ':punch::skin-tone-5:'
        highestt = max(highest)
        for check in contestants:
            if str(highestt) in check:
                winners.append(check.split(':', 1)[0])
        await ctx.send(f'``And The Winners Are:`` :balloon: ``{", ".join(winners)}`` :balloon:')


@client.command(aliases=['8ball'])
async def __8ball__(ctx, *, question):
    channel = ctx.message.author.voice.channel
    global vc
    vc = await channel.connect()
    vc.play(discord.FFmpegPCMAudio("8ball.mp3"), after=lambda e: print('done', e))
    while vc.is_playing():
        await asyncio.sleep(1)
    await vc.disconnect()
    answers = [
        'Yes.',
        'No.',
        'maybe.',
        'I hope so.',
        "I don't think so.",
        "I'm pretty sure it's false.",
        'Yes daddy.',
        'No daddy.',
        "Yes mommy it's right.",
        'It is certain.',
        "It is decidedly so.",
        "Without a doubt.",
        "Yes - definitely.",
        "You may rely on it.",
        "As I see it, yes.",
        "Most likely.",
        "Outlook good.",
        "Signs point to yes.",
        "Reply hazy, try again.",
        "Ask again later.",
        "Better not tell you now.",
        "Cannot predict now.",
        "Concentrate and ask again.",
        "Don't count on it.",
        "My reply is no.",
        "My sources say no.",
        "Outlook not so good.",
        "Very doubtful."
    ]
    await ctx.send(f' :8ball: ``Question: {question}`` :8ball:\n \n:8ball: ``Answer: {random.choice(answers)}`` :8ball:')


@client.command()
async def screen(ctx):
    screen = ImageGrab.grab(bbox=None)
    screen.save('screen.png')
    await ctx.send(file=discord.File(fp="screen.png"))


@client.command()
async def _laughearrape(ctx):
    win = None
    while win == None:
        win = locateOnScreen('win.png', grayscale=True, confidence=0.8)

    winc = center(win)

    click(winc[0], winc[1])

    typewrite('google chrome')

    await asyncio.sleep(1)

    press('enter')

    await asyncio.sleep(2)

    typewrite('https://www.youtube.com/watch?v=D4bsRnFX4-k')

    await asyncio.sleep(1)

    press('enter')

    await asyncio.sleep(2)

    screens = ImageGrab.grab(bbox=None)
    screens.save('screen.png')
    await ctx.send(file=discord.File(fp="screen.png"))

@client.event
async def on_reaction_add(reaction, user):
    global reauser
    reauser = user

@client.command()
async def _69calc(ctx):
    ohad = ctx.message.author.name
    if ohad.lower() == "kittisama":
        await ctx.send("```NO!```")
    else:
        win = None
        while win == None:
            win = locateOnScreen('win.png', grayscale=True, confidence=0.8)

        winc = center(win)

        click(winc[0], winc[1])

        typewrite('calculator')

        press('enter')

        sleep(1)

        sbtn = None
        while sbtn == None:
            sbtn = locateOnScreen('6btn.png', grayscale=True, confidence=0.9)

        sbtnc = center(sbtn)

        click(sbtnc[0], sbtnc[1])

        nbtn = None
        while nbtn == None:
            nbtn = locateOnScreen('9btn.png', grayscale=True, confidence=0.9)

        nbtnc = center(nbtn)

        click(nbtnc[0], nbtnc[1])

        screens = ImageGrab.grab(bbox=None)
        screens.save('screen.png')
        await ctx.send(file=discord.File(fp="screen.png"))

guess = False

@client.command()
async def hangman(ctx, *, message):

    with open('food.txt', 'r') as food:
        food_read = food.read()
        food_list = food_read.split('\n')

    with open('movies.txt', 'r') as movie:
        movie_read = movie.read()
        movie_list = movie_read.split('\n')

    global guess
    if not guess and message.lower() == 'food' or message.lower() == 'movies':

        global game_choice
        game_choice = message.lower()

        if game_choice == 'food':

            game_choice = food_list

        else:

            game_choice = movie_list

        global lives
        lives = 5
        global game_board
        game_board = []
        global word
        word = random.choice(game_choice)

        x = 1

        while x <= len(word):
            game_board.append('\\_')

            x += 1

        letter_index = 0
        for letter in word:

            if letter == ' ':
                game_board[letter_index] = ' '

            letter_index += 1

        await ctx.send(' '.join(game_board))

        guess = True

    elif guess and len(message) == 1:

        guess = message.lower()

        wrong_guess = True

        letter_index = 0
        for letter in word:

            if letter == guess:
                game_board[letter_index] = guess
                wrong_guess = False

            letter_index += 1

        await ctx.send(' '.join(game_board))

        if wrong_guess:
            lives -= 1
            await ctx.send(f'You have {lives} lives left!')

            if lives == 0:
                await ctx.send(f'You lost! the word was {word}')
                guess = False

        if '\\_' not in game_board:
            await ctx.send(f'You won! the word was {word}!')
            guess = False

    else:
        await ctx.send('Please write food or movies or guess a letter!')


@client.command()
async def ping(ctx):
    await ctx.send(f':ping_pong: ``Pong:`` ``{round(client.latency*1000)}ms`` :ping_pong:')


@client.command(aliases=['disconnect'])
async def logout(ctx):
    await client.close()


client.run('NTIyNDM4ODM0ODEwNTE5NTUy.XPvAdg.DXmiOt8UtnbB6FxgFlvTjJJVusA')