import discord
import basil
from bot import Bot

client = discord.Client()
bot = bot.Bot(client)

bot.add_command('basil', basil)



@client.async_event
def on_message(message):
    if message.author == client.user:
        return
    bot.compregend(message)
