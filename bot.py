import os
import discord

from dotenv import load_dotenv
from discord.ext import commands


load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')

bot = commands.Bot(command_prefix='!')

@bot.event
async def on_ready():
    print(f'{bot.user} has connected to Discord!')

@bot.command(name='hb')
async def happy_birthday(ctx):
    response = 'Happy Birthday! 🎈🎉'
    await ctx.send(response)

bot.run(TOKEN)
