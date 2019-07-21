#!/usr/bin/python3
import subprocess
import discord
import threading
import time
import os

from libbasil_I2C import *


DISCORD_TOKEN = os.environ['DISCORD_TOKEN']

HELPTEXT='''Commands:
(basil pay respects)
(basil play [SONG])
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

@client.event
async def on_ready():
    print('Logged in as')
    print(client.user.name)
    print(client.user.id)
    print('------')

client.run(DISCORD_TOKEN)
