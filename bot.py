import os
import discord
import requests
import json
import ast

from dotenv import load_dotenv
from discord.ext import commands


load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')

bot = commands.Bot(command_prefix='!')

# On join
@bot.event
async def on_ready():
    print(f'{bot.user} connected to Discord.')


# Commands
@bot.command(name='hb')
async def happy_birthday(ctx):
    response = 'Happy Birthday! 🎈🎉'
    await ctx.send(response)

@bot.command(name='api')
async def api_test(ctx):
    response = requests.get('https://pokeapi.co/api/v2/berry/1')
    await ctx.send("Attempted.")
    await ctx.send(response.status_code)
    if response.status_code == 200:
        text = json.dumps(response.json(), sort_keys=True)
        data = ast.literal_eval(text)
        await ctx.send(data.keys())
        await ctx.send("Success.")
    elif response.status_code > 400:
        await ctx.send('Connection failed.')
        await ctx.send('Status code: ', response.status_code)

@bot.command(name='echo')
async def echo(ctx):
    response = ctx.message.content.replace(ctx.message.content.split()[0] + " ", '')
    await ctx.send(response)


# Shut down
@bot.command(name='quit')
async def quit(ctx):
    response = 'Shutting down...'
    await ctx.send(response)
    await bot.close()

# run bot
bot.run(TOKEN)
