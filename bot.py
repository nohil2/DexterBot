import asyncio
import os
import discord
import requests
import json
import random as rand
from PIL import Image
from io import BytesIO
import time

from dotenv import load_dotenv
from discord.ext import commands

# global values
wtp_lock = False

load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')

bot = commands.Bot(command_prefix='!')

# on join
@bot.event
async def on_ready():
    print(f'{bot.user} connected to Discord.')


# commands
@bot.command()
async def ping(ctx):
    """
    Ping
    """
    response = 'Ready to go!'
    await ctx.send(response, delete_after=10)




@bot.command(name='dex')
async def pokemon_search(ctx):
    """
    Search for a Pokedex entry

    Dexter Bot looks up a Pokemon based on your input, by either National Dex number or name
    """ 

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

        # get pokemon name and national dex number 
        name = jsondata['name'].capitalize()
        dex_number = str(jsondata_species['pokedex_numbers'][0]['entry_number'])
        name = '**'+name+'\t#'+dex_number+'**'

        # get pokemon types
        num_types = 0
        for x in pokemon_types:
             num_types+=1

        if num_types == 2: 
            types = pokemon_types[0]['type']['name'].capitalize()+' / '+pokemon_types[1]['type']['name'].capitalize()
        elif num_types == 1:
            types = pokemon_types[0]['type']['name'].capitalize()
        types = types

        # get official artwork
        image_url = jsondata['sprites']['other']['official-artwork']['front_default']
        # resize image to save on screen space in chat
        image = Image.open(requests.get(image_url, stream=True).raw)
        image = image.resize((200,200))
        tempfile = BytesIO()
        image.save(tempfile, format='png')
        image.close()

        # get and choose random pokedex entry (in english)
        temp = []
        for entry in dex_entries:
            if entry['language']['name'] == 'en':
                temp.append(entry['flavor_text'].replace('\n', ' ').replace('\x0c', ' '))

        rand.seed()
        dex_text = rand.choice(temp)
        dex_text = '```'+dex_text+'```'

        # display all of the above
        await ctx.send(name)
        await ctx.send(types)
        await ctx.send(dex_text)
        await ctx.send(image)

@bot.command(name='rdex')
async def random_pokemon(ctx):
    """
    Random Pokedex entry

    Dexter Bot looks up a random Pokemon
    """

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

        image_url = jsondata['sprites']['other']['official-artwork']['front_default']
        image = Image.open(requests.get(image_url, stream=True).raw)
        image = image.resize((200,200))
        tempfile = BytesIO()
        image.save(tempfile, format='png')
        image.close()

        temp = []
        for entry in dex_entries:
            if entry['language']['name'] == 'en':
                temp.append(entry['flavor_text'].replace('\n', ' ').replace('\x0c', ' '))

        dex_text = rand.choice(temp)
        dex_text = '```'+dex_text+'```'

        await ctx.send(name)
        await ctx.send(types)
        await ctx.send(dex_text)
        tempfile.seek(0)
        await ctx.send(file=discord.File(tempfile, 'pokemon.png'))
        

@bot.command()
async def wtp(ctx):
    """
    Who's that Pokemon?
    """
    # check if command is already running
    global wtp_lock
    if wtp_lock == True:
        return
    else:
        wtp_lock = True

    rand.seed()
    random_num = str(rand.randint(1, 898))
    
    response = requests.get('https://pokeapi.co/api/v2/pokemon/'+random_num)
    if response.status_code > 400:
        await ctx.send('Connection failed.')
        fail_string = 'Status codes: '+str(response.status_code)
        await ctx.send(fail_string)
    elif response.status_code == 200:
        jsondata = json.loads(response.text)
        name = jsondata['name'].replace('-', ' ')
        image_url = jsondata['sprites']['other']['official-artwork']['front_default']
        
        # use PIL to create silhoutte of artwork and create a byte stream of silhouette
        image = Image.open(requests.get(image_url, stream=True).raw)
        image = image.resize((200,200))
        temp = BytesIO()
        image.save(temp, format='png')
        alpha = image.getchannel('A')
        silhouette = Image.new('RGBA', image.size, color='black')
        silhouette.putalpha(alpha)
        tempfile = BytesIO()
        silhouette.save(tempfile, format='png')

        await ctx.send("**Who's that Pokemon?**")
        tempfile.seek(0)
        await ctx.send(file=discord.File(tempfile, 'silhouette.png'))
        image.close()
        silhouette.close()
        start_time = time.time()

        # check channel for name of pokemon
        def check(message):
            return name in message.content.lower() and message.channel == ctx.channel
        
        msg = await bot.wait_for("message", check=check)
        total_time = time.time() - start_time
        await ctx.send(f"{msg.author.mention} got it right in **{total_time:.2f} seconds!** It's **{name.capitalize()}!**")
        await ctx.send(file=discord.File(temp, 'pokemon.png'))

    # allows command to run after finished
    wtp_lock = False


# Shut down
@bot.command(name='q')
@commands.has_permissions(administrator=True)
async def quit(ctx):
    """
    Shuts down Dexter Bot
    """
    response = 'Shutting down...'
    await ctx.send(response)

    # shut down
    loop = bot.loop
    await bot.close()
    await loop.stop()
    pending = asyncio.Task.all_tasks()
    await loop.run_until_complete(asyncio.gather(*pending))
    bot.close()
    raise SystemExit

# run bot
bot.run(TOKEN)