@client.command()
async def terraria(ctx, *, message):
    Items = []
    path = 'C:/Users/amikr/OneDrive/מסמכים/python/All Terraria Sounds'
    for sound in listdir(path):
        Items.append(sound)

    if 'music' in message.lower():
        amount = int(message.replace(' music', ''))
    else:
        amount = int(message)
    x = 0
    toPlay = []
    global queue
    queue = []
    while x <= amount:
        rand = random.choice(Items)
        if 'music' in message.lower():
            if '.wav' in rand:
                continue
            else:
                if x == 0:
                    queue.append('Now Playing: ' + rand + '\n\n')
                else:
                    queue.append(str(x) + ': ' + rand + '\n')
                toPlay.append(rand)
                x += 1
        else:
            if x == 0:
                queue.append('Now Playing: ' + rand + '\n\n')
            else:
                queue.append(str(x) + ': ' + rand + '\n')
            toPlay.append(rand)
            x += 1
    channel = ctx.message.author.voice.channel
    global vc
    vc = await channel.connect()
    a = await ctx.send(":speaker: ``Now Playing: `` :speaker:")
    breakl = 0
    x = 1
    for play in toPlay:
        if breakl == 1:
            break
        await a.add_reaction(emoji='⏹')
        await a.add_reaction(emoji='⏸')
        await a.add_reaction(emoji='⏩')
        await a.edit(content=f":speaker: ``Now Playing: {play}`` :speaker:")
        vc.play(discord.FFmpegPCMAudio(path+'/'+play), after=lambda e: print('done', e, play))
        while vc.is_playing():
            message = await a.channel.fetch_message(a.id)
            countstop = message.reactions[0].count
            countpause = message.reactions[1].count
            countskip = message.reactions[2].count
            if countstop == 2:
                breakl = 1
                vc.stop()
                break
            if countskip == 2:
                await a.remove_reaction('⏩', reauser)
                vc.stop()
                break
            if countpause == 2:
                vc.pause()
                while countpause > 1:
                    if countpause == 3:
                        await a.remove_reaction('⏸', reauser)
                    message = await a.channel.fetch_message(a.id)
                    countpause = message.reactions[1].count
                vc.resume()
            await asyncio.sleep(1)
        queue.remove(queue[0])
        y = 0
        while y <= amount-x:
            if y == 0:
                new = queue[y].replace(str(y + 1), 'Now Playing', 1)
                new += '\n'
            else:
                new = queue[y].replace(str(y+1), str(y), 1)
            queue[y] = new
            y += 1
        x += 1
    await vc.disconnect()