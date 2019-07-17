#!/usr/bin/python3
import subprocess
import discord
import threading
import time
import os

from libbasil import *


DISCORD_TOKEN = os.environ['DISCORD_TOKEN']

HELPTEXT='''Commands:
(basil pay respects)
(basil play [SONG])
!basil moisture
!basil history
!basil help
!basil flip the table
!basil chuck a yeet
'''



client=discord.Client()

@client.event
async def on_message(message):
    # we do not want the bot to reply to itself
    if message.author == client.user:
        return

    content = message.content.lower()

    if 'basil pay respects' in content:
        msg = 'F'
        await message.channel.send(msg)

    elif 'basil play' in content:
        p = subprocess.Popen(["/usr/bin/omxplayer",
            "--no-keys",
            "/home/pi/music/.despacito.mp3"],
            stderr=subprocess.STDOUT)

        msg = 'Now playing: Despacito ft. Daddy Yankee'
        await message.channel.send(msg)

    elif content.startswith('!basil') or content.startswith('basil,'):
        cmd = content[7:]
        msg = HELPTEXT

        if cmd.startswith('moisture'):
            msg = "Soil moisture content: {:.1f}%\n".format(getMoisture())

        elif cmd.startswith('history'):
            num = 12
            try:
                num = int(message.content[len('!basil history'):])
            except ValueError:
                pass
            msg = getHistory(num)


        elif cmd.startswith('water'):
            # NOTE: This needs a heuristic model of soil moisture
            tau = 5
            try:
                tau = int(message.content[len('!basil water'):])
            except ValueError:
                tau=5

            if tau > 60:
                msg= 'You may not water for more than 1 minute.'
            elif tau <0:
                msg= "Nice try, you won't fool me with that one again"
            else:
                moisture = getMoisture()
                if moisture > 70:
                    msg = 'You should not water me any more, the soil is '
                    msg += 'already {:.1f}% damp'.format(moisture)
                else:
                    pumpPulse(tau)
                    msg = "{} seconds of S i p p\n".format(tau)

        elif cmd.startswith('please run the motherfucking pump'):
            # the super secret override message. Don't tell anyone.
            pumpPulse(1)
            msg = "{} seconds of S i p p\n".format(tau)
        elif cmd.startswith('chuck a yeet'):
            msg='(╯°□°）╯︵ YEET'
        elif cmd.startswith('flip the table'):
            msg='(╯°□°）╯︵ ┻━┻'
        await message.channel.send(msg)

@client.event
async def on_ready():
    print('Logged in as')
    print(client.user.name)
    print(client.user.id)
    print('------')

client.run(DISCORD_TOKEN)
