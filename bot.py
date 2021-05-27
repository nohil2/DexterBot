from asyncio.windows_events import NULL
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
async def ping(ctx):
    response = 'Ready to go!'
    await ctx.send(response)

@bot.command(name='api')
async def api_test(ctx):
    response = requests.get('https://pokeapi.co/api/v2/pokemon/1')
    response_species = requests.get('https://pokeapi.co/api/v2/pokemon-species/1')
    if response.status_code == 200 and response_species.status_code == 200:
        jsondata = json.loads(response.text)
        jsondata_species = json.loads(response_species.text)

        pokemon_types = jsondata.get('types')
        dex_entries = jsondata_species.get('flavor_text_entries')

        name = jsondata['name'].capitalize()
        name = '**'+name+'**'

        num_types = 0
        for x in pokemon_types:
            num_types+=1

        if num_types == 2: 
            types = pokemon_types[0]['type']['name'].capitalize()+' / '+pokemon_types[1]['type']['name'].capitalize()
        elif num_types == 1:
            types = pokemon_types[0]['type']['name'].capitalize()
        types = '*'+types+'*'

        image = jsondata['sprites']['other']['official-artwork']['front_default']

        for entry in dex_entries:
            if entry['language']['name'] == 'en':
                dex_text = entry['flavor_text'].replace('\n', ' ').replace('\x0c', ' ')
                break
        dex_text = '```'+dex_text+'```'

        await ctx.send(name)
        await ctx.send(types)
        await ctx.send(dex_text)
        await ctx.send(image)

    elif response.status_code > 400:
        await ctx.send('Connection failed.')
        fail_string = 'Status codes: '+str(response.status_code)+', '+str(response_species.status_code)
        await ctx.send(fail_string)

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
