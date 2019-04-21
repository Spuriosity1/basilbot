#!/usr/bin/python3
import subprocess
import discord
import threading
import serial
import csv
import struct
import time
import os


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

def convert_moisture_raw(raw):
    return 100 * raw / 500

def sample_data(ser, N):
    data = [0]
    ser.reset_input_buffer()
    for i in range(0,N):
        ser.write(b'X\n')
        res = ser.readline().strip(b'\r\n').split(b'|')
        data = [ x[0] + int(x[1]) for x in zip(data, res) ]

    retval = [ x/N for x in data]
    retval[0] = convert_moisture_raw(retval[0])
    return retval


def pumpPulse(ser, speed, power):
    ser.write(b'S')
    ser.write(struct.pack('<B',speed))
    ser.write(struct.pack('<H',power))
    ser.write(b'\n')
    print(ser.readline())


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
            with serial.Serial(port='/dev/ttyACM0', dsrdtr=True,
                                baudrate=9600) as ser:
                moisture = sample_data(ser, 5)[0]
            msg = "Soil moisture content: {:.1f}%\n".format(moisture)

        elif cmd.startswith('history'):
            lines = [];
            num = 12
            with open('../data/history.csv','r') as f:
                reader = csv.reader(f,delimiter=',')
                lines = [row for row in reader]
            try:
                num = int(message.content[len('!basil history'):])
            except ValueError:
                pass

            msg = "Date \t\t| \t moisture\n"
            for row in lines[-num:]:

                msg += '{} \t\t| \t {:.1f}\n'.format(row[0].replace('T',' '), float(row[1])/5)

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
                with serial.Serial(port='/dev/ttyACM0', dsrdtr=True,
                                    baudrate=9600) as ser:
                    moisture= sample_data(ser, 5)[0]

                    if moisture > 70:
                        msg = 'You should not water me any more, the soil is '
                        msg += 'already {:.1f}% damp'.format(moisture)
                    else:
                        pumpPulse(ser, 255, tau*1000)
                        msg = "{} seconds of S i p p\n".format(tau)

        elif cmd.startswith('please run the motherfucking pump'):
            # the super secret override message. Don't tell anyone.
            pumpPulse(ser, 255, tau*1000)
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
