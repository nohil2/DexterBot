import os
import discord
import requests
import json

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
@bot.command(name='ping')
async def happy_birthday(ctx):
    response = 'Ready to go!'
    await ctx.send(response)

@bot.command(name='api')
async def api_test(ctx):
    response = requests.get('https://pokeapi.co/api/v2/pokemon/1')
    if response.status_code == 200:
        data = json.loads(response.text)
        temp = data.get('types')
        await ctx.send(data.get('name').capitalize())
        await ctx.send(temp[0]['type']['name'].capitalize()+' / '+temp[1]['type']['name'].capitalize())
    elif response.status_code > 400:
        await ctx.send('Connection failed.')
        await ctx.send('Status code: ', response.status_code)

# @bot.command(name='echo')
# async def echo(ctx):
#     response = ctx.message.content.replace(ctx.message.content.split()[0] + " ", '')
#     await ctx.send(response)


# Shut down
@bot.command(name='q')
async def quit(ctx):
    response = 'Shutting down...'
    await ctx.send(response)
    await bot.close()

# run bot
bot.run(TOKEN)
