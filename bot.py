import os
import discord
import requests
import json
import random as rand

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

@bot.command(name='dex')
async def pokemon_search(ctx):
    search_term = ctx.message.content.replace(ctx.message.content.split()[0] + " ", '')
    if search_term.isnumeric():
        if int(search_term) > 898:
            await ctx.send("There's no Pokemon with that Dex Number; try again.")
        response = requests.get('https://pokeapi.co/api/v2/pokemon/'+search_term)
        response_species = requests.get('https://pokeapi.co/api/v2/pokemon-species/'+search_term)
    else:
        response = requests.get('https://pokeapi.co/api/v2/pokemon/'+search_term.lower())
        response_species = requests.get('https://pokeapi.co/api/v2/pokemon-species/'+search_term.lower())
    if response.status_code > 400 and response_species.status_code > 400:
         if response.status_code == 404:
            await ctx.send('No Pokemon with that name; try again.')
         else:
            await ctx.send('Connection failed.')
            fail_string = 'Status codes: '+str(response.status_code)+', '+str(response_species.status_code)
            await ctx.send(fail_string)
    elif response.status_code == 200 and response_species.status_code == 200:
        jsondata = json.loads(response.text)
        jsondata_species = json.loads(response_species.text)

        pokemon_types = jsondata.get('types')
        dex_entries = jsondata_species.get('flavor_text_entries')

        name = jsondata['name'].capitalize()
        dex_number = str(jsondata_species['pokedex_numbers'][0]['entry_number'])
        name = '**'+name+'\t#'+dex_number+'**'

        num_types = 0
        for x in pokemon_types:
             num_types+=1

        if num_types == 2: 
            types = pokemon_types[0]['type']['name'].capitalize()+' / '+pokemon_types[1]['type']['name'].capitalize()
        elif num_types == 1:
            types = pokemon_types[0]['type']['name'].capitalize()
        types = types

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

@bot.command(name='rdex')
async def random_pokemon(ctx):
    rand.seed()
    random_num = str(rand.randint(1, 898))
    
    response = requests.get('https://pokeapi.co/api/v2/pokemon/'+random_num)
    response_species = requests.get('https://pokeapi.co/api/v2/pokemon-species/'+random_num)

    if response.status_code > 400 and response_species.status_code > 400:
        await ctx.send('Connection failed.')
        fail_string = 'Status codes: '+str(response.status_code)+', '+str(response_species.status_code)
        await ctx.send(fail_string)
    elif response.status_code == 200 and response_species.status_code == 200:
        jsondata = json.loads(response.text)
        jsondata_species = json.loads(response_species.text)

        pokemon_types = jsondata.get('types')
        dex_entries = jsondata_species.get('flavor_text_entries')

        name = jsondata['name'].capitalize()
        dex_number = str(jsondata_species['pokedex_numbers'][0]['entry_number'])
        name = '**'+name+'\t#'+dex_number+'**'

        num_types = 0
        for x in pokemon_types:
             num_types+=1

        if num_types == 2: 
            types = pokemon_types[0]['type']['name'].capitalize()+' / '+pokemon_types[1]['type']['name'].capitalize()
        elif num_types == 1:
            types = pokemon_types[0]['type']['name'].capitalize()
        types = types

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

# Shut down
@bot.command(name='q')
async def quit(ctx):
    response = 'Shutting down...'
    await ctx.send(response)
    await bot.close()

# run bot
bot.run(TOKEN)
